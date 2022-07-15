from termcolor import colored
from datetime import datetime
from calendar import monthrange

from sqlalchemy import create_engine, update
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

from app.packages import RequestExpress, MailExpress
from app.database.models import Coleta, DeclarativeBase

from app.configurations import ProductionConfig

engine = create_engine(ProductionConfig.DATABASE_URI)


def init_db():
    DeclarativeBase.Model.metadata.create_all(bind=engine)


def insert_data_on_table():
    mail = MailExpress(
        'smtp.mailtrap.io',
        2525,
        'e46dc7ab483db9',
        '66f0eabf5ff39d'
    )

    try:
        date = f'{datetime.now().day - 1}/{datetime.now().month:02d}/{datetime.now().year}'

        print(
            f'⚠️ {colored("ATENÇÃO:", "red")} Início do processo de atualização do banco de dados.\n'
            f'Fazendo a requisição ao {colored("ESL", "blue")} dos dados da data atual: {colored(date, "green")}.\n'
        )

        request = RequestExpress(
            'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw'
        )
        response = request.get_template_from_date(date)

        print(
            f'⚠️ {colored("ATENÇÃO:", "red")} Requisição dos dados do {colored("ESL", "blue")} efetuada com sucesso. '
            f'Executaremos o update diário do banco de dados com os relatórios.\n'
            f'{colored("Pode ocorrer microlentidão ou travamentos durante o processo", "red")}.\n'
        )

        try:
            # For every item who is inside response we create a new class<Model> Coleta and insert informations who is into data.
            # After that we add the new class Coleta to the database, commit and close the cursor.
            for item in response:
                with Session(engine) as session:
                    item['esl_id'] = item['id']
                    del item['id']

                    try:
                        collect = Coleta(**item)
                        collect_exists = session.query(Coleta).filter_by(
                            fit_fis_id=item['fit_fis_id']).first()

                        if collect_exists:
                            values = collect.to_dict()
                            del values['id']
                            smtp = update(Coleta).where(
                                Coleta.fit_fis_id == item['fit_fis_id']).values(values)
                            session.execute(smtp)
                        else:
                            session.add(collect)
                    except:
                        fields_who_not_exists = [
                            field for field in item if field not in Coleta()._keys()]

                        for field in fields_who_not_exists:
                            Coleta()._add_column(field, item[field])

                            if type(item[field]) is str:
                                session.query(
                                    text(f'ALTER TABLE coletas'
                                        f'ADD COLUMN {field} varchar(150);')
                                )
                            else:
                                session.query(
                                    text(f'ALTER TABLE coletas'
                                        f'ADD COLUMN {field} int;')
                                )

                        collect = Coleta(**item)
                        collect_exists = session.query(Coleta).filter_by(
                            fit_fis_id=item['fit_fis_id']).first()

                        if collect_exists:
                            values = collect.to_dict()
                            del values['id']
                            smtp = update(Coleta).where(
                                Coleta.fit_fis_id == item['fit_fis_id']).values(values)
                            session.execute(smtp)
                        else:
                            session.add(collect)

                    # Final da lógica do for.
                    session.commit()

            # Todo: Send a mail notification for the operador informing about the success of this operation.
            subject = 'Informativo sobre a atualização do ESL'
            message = 'Bom dia! Os dados de hoje foram atualizados com sucesso.'

            mail.send_informative_message(
                'Rodrigo Siliunas <rodrigo.cunha@viaexpress.com>',
                'Claudio Ferreira <claudio.ferreira@viaexpress.com>',
                subject,
                message
            )

            print(
                f'✔️ {colored("SUCESSO:", "green")} O banco de dados foi atualizado com sucesso.\n'
                f'Um email informativo foi disparado ao operador. Próxima atualização no mesmo horário amanhã.\n'
            )
        except Exception as e:
            # Todo: Send a mail notification for this error.
            subject = 'Falha na Atualização: Banco de Dados'
            message = 'Ocorreu um erro na atualização do banco de dados da empresa. Comunique o setor de TI.'

            mail.send_informative_message(
                'Rodrigo Siliunas <rodrigo.cunha@viaexpress.com>',
                'Claudio Ferreira <claudio.ferreira@viaexpress.com>',
                subject,
                message
            )

            print(
                f'🚫 {colored("ATENÇÃO:", "red")} Ocorreu um erro durante a execução da atualização diária do banco de dados.\n'
                f'Um {colored("E-MAIL", "green")} acaba de ser enviado para o operador informando o ocorrido.\n'
            )

            print(e)
    except:
        subject = 'Falha na requisição dos dados da ESL'
        message = 'Bom dia. A requisição aos dados da ESL falhou.\n' \
            'Houve problema no servidor deles. Por gentileza, comunique o setor de TI ou se preferir aguarde até amanhã.'.strip()

        mail.send_informative_message(
            'Rodrigo Siliunas <rodrigo.cunha@viaexpress.com>',
            'Claudio Ferreira <claudio.ferreira@viaexpress.com>',
            subject,
            message
        )

        print(
            f'🚫 {colored("ATENÇÃO:", "red")} Um erro ocorreu na requisição dos dados.\n'
            f'Problema com o {colored("ESL", "blue")}. Informar ao setor de TI.\n'
        )


def insert_all_data_on_table():
    mail = MailExpress(
        'smtp.mailtrap.io',
        2525,
        'e46dc7ab483db9',
        '66f0eabf5ff39d'
    )

    try:
        for month in range(1, datetime.now().month + 1):
            mounth_days = monthrange(2022, month)[1]

            for day in range(1, mounth_days + 1):
                date = f'{day:02d}/{month:02d}/{datetime.now().year}'

                print(
                    f'⚠️ {colored("ATENÇÃO:", "red")} Início do processo de atualização do banco de dados.\n'
                    f'Fazendo a requisição ao {colored("ESL", "blue")} dos dados da data atual: {colored(date, "green")}.\n'
                )

                request = RequestExpress(
                    'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw'
                )
                response = request.get_template_from_date(date)

                try:
                    print(
                        f'⚠️ {colored("ATENÇÃO:", "red")} Requisição dos dados do {colored("ESL", "blue")} efetuada com sucesso. '
                        f'Executaremos o update diário do banco de dados com os relatórios.\n'
                        f'{colored("Pode ocorrer microlentidão ou travamentos durante o processo", "red")}.\n'
                    )

                    # For every item who is inside response we create a new class<Model> Coleta and insert informations who is into data.
                    # After that we add the new class Coleta to the database, commit and close the cursor.
                    for item in response:
                        with Session(engine) as session:
                            item['esl_id'] = item['id']
                            del item['id']

                            collect = Coleta(**item)
                            collect_exists = session.query(Coleta).filter_by(
                                fit_fis_id=item['fit_fis_id']).first()

                            if collect_exists:
                                values = collect.to_dict()
                                del values['id']

                                smtp = update(Coleta).where(Coleta.fit_fis_id == item['fit_fis_id']).values(values)
                                session.execute(smtp)
                            else:
                                session.add(collect)

                            session.commit()

                    # Todo: Send a mail notification for the operador informing about the success of this operation.
                    subject = 'Informativo sobre a atualização do ESL'
                    message = 'Bom dia! Os dados de hoje foram atualizados com sucesso.'

                    mail.send_informative_message(
                        'Rodrigo Siliunas <rodrigo.cunha@viaexpress.com>',
                        'Claudio Ferreira <claudio.ferreira@viaexpress.com>',
                        subject,
                        message
                    )

                    print(
                        f'✔️ {colored("SUCESSO:", "green")} O banco de dados foi atualizado com sucesso.\n'
                        f'Um email informativo foi disparado ao operador. Próxima atualização no mesmo horário amanhã.\n'
                    )
                except Exception as e:
                    # Todo: Send a mail notification for this error.
                    subject = 'Falha na Atualização: Banco de Dados'
                    message = 'Ocorreu um erro na atualização do banco de dados da empresa. Comunique o setor de TI.'

                    mail.send_informative_message(
                        'Rodrigo Siliunas <rodrigo.cunha@viaexpress.com>',
                        'Claudio Ferreira <claudio.ferreira@viaexpress.com>',
                        subject,
                        message
                    )

                    print(
                        f'🚫 {colored("ATENÇÃO:", "red")} Ocorreu um erro durante a execução da atualização diária do banco de dados.\n'
                        f'Um {colored("E-MAIL", "green")} acaba de ser enviado para o operador informando o ocorrido.\n'
                    )

                    print(e)
    except:
        subject = 'Falha na requisição dos dados da ESL'
        message = 'Bom dia. A requisição aos dados da ESL falhou.\n' \
            'Houve problema no servidor deles. Por gentileza, comunique o setor de TI ou se preferir aguarde até amanhã.'.strip()

        mail.send_informative_message(
            'Rodrigo Siliunas <rodrigo.cunha@viaexpress.com>',
            'Claudio Ferreira <claudio.ferreira@viaexpress.com>',
            subject,
            message
        )

        print(
            f'🚫 {colored("ATENÇÃO:", "red")} Um erro ocorreu na requisição dos dados.\n'
            f'Problema com o {colored("ESL", "blue")}. Informar ao setor de TI.\n'
        )
