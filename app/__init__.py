import os
from termcolor import colored
from datetime import datetime
from calendar import monthrange

from sqlalchemy import create_engine, update
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

from app.packages import RequestExpress, MailExpress
from app.database.models import Coleta, DeclarativeBase

from app.configurations import DevelopmentConfig

engine = create_engine(DevelopmentConfig.DATABASE_URI)


def init_db():
    DeclarativeBase.Model.metadata.create_all(bind=engine)


def insert_data_without_update(from_date: str, to_date: str):
    print(
        f'⚠️ {colored("ATENÇÃO:", "red")} Início do processo de atualização do banco de dados.\n'
        f'Fazendo a requisição ao {colored("ESL", "blue")} dos dados de {colored(from_date, "green")} até '
        f'{colored(to_date, "green")}.\n'
    )

    try:
        request = RequestExpress(
            'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw'
        )
        response = request.get_template_from_date_to_date(from_date, to_date)

        print(
            f'⚠️ {colored("ATENÇÃO:", "red")} Requisição dos dados do {colored("ESL", "blue")} efetuada com sucesso. '
            f'Executaremos o update diário do banco de dados com os relatórios.\n'
            f'{colored("Pode ocorrer microlentidão ou travamentos durante o processo", "red")}.\n'
        )
    except:
        print(
            f'🚫 {colored("ATENÇÃO:", "red")} Ocorreu um erro durante a execução da atualização diária do banco de dados.\n'
            f'Um {colored("E-MAIL", "green")} acaba de ser enviado para o operador informando o ocorrido.\n'
        )
        return False

    # For every item who is inside response we create a new class<Model> Coleta and insert informations who is into data.
    # After that we add the new class Coleta to the database, commit and close the cursor.
    for item in response:
        with Session(engine) as session:
            item['esl_id'] = item['id']
            del item['id']

            try:
                collect_exists = session.query(Coleta).filter_by(
                    fit_fis_id=item['fit_fis_id']).first()

                if ((not item['fit_fis_ioe_number']) and (collect_exists)):
                    values = collect.to_dict()
                    del values['id']

                    smtp = update(Coleta).where(
                        Coleta.fit_fis_id == item['fit_fis_id']).values(values)
                    session.execute(smtp)

                collect = Coleta(**item)
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
                session.add(collect)

            # Final da lógica do for.
            session.commit()

    print(
        f'✔️ {colored("SUCESSO:", "green")} O banco de dados foi atualizado com sucesso.\n'
        f'Um email informativo foi disparado ao operador. Próxima atualização no mesmo horário amanhã.\n'
    )


def insert_from_data_to_data(from_date: str, to_date: str):
    print(
        f'⚠️ {colored("ATENÇÃO:", "red")} Início do processo de atualização do banco de dados.\n'
        f'Fazendo a requisição ao {colored("ESL", "blue")} dos dados de {colored(from_date, "green")} até '
        f'{colored(to_date, "green")}.\n'
    )

    try:
        request = RequestExpress(
            'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw'
        )
        response = request.get_template_from_date_to_date(from_date, to_date)

        print(
            f'⚠️ {colored("ATENÇÃO:", "red")} Requisição dos dados do {colored("ESL", "blue")} efetuada com sucesso. '
            f'Executaremos o update diário do banco de dados com os relatórios.\n'
            f'{colored("Pode ocorrer microlentidão ou travamentos durante o processo", "red")}.\n'
        )
    except:
        print(
            f'🚫 {colored("ATENÇÃO:", "red")} Ocorreu um erro durante a execução da atualização diária do banco de dados.\n'
            f'Um {colored("E-MAIL", "green")} acaba de ser enviado para o operador informando o ocorrido.\n'
        )
        return False

    row_added_count, row_edited_count, row_error_count = 0, 0, 0

    # For every item who is inside response we create a new class<Model> Coleta and insert informations who is into data.
    # After that we add the new class Coleta to the database, commit and close the cursor.
    for item in response:
        with Session(engine) as session:
            item['esl_id'] = item['id']
            del item['id']

            try:
                collect = Coleta(**item)
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

            fit_fis_id_exists = session.query(Coleta).filter_by(
                fit_fis_id=item['fit_fis_id']).first()
            esl_id_exists = session.query(Coleta).filter_by(
                esl_id=item['esl_id']).first()

            # Se o campo FIT_FIS_ID for 'NULL' E existir o número ESL_ID desse item no banco de dados, então atualizamos com as informações do item onde ESL_ID for igual a ESL_ID;
            if ((item['fit_fis_ioe_number'] is None) or (item['fit_fis_ioe_number'] == "")):
                values = collect.to_dict()
                del values['id']

                if (esl_id_exists):
                    smtp = update(Coleta).where(
                        Coleta.esl_id == item['esl_id']).values(values)
                    session.execute(smtp)

                    row_edited_count += 1
                    continue

            # Se no banco de dados existir um número igual ao FIT_FIS_ID do item, então atualizamos com o valor desse novo item declarado onde o FIT_FIS_ID for igual a FIT_FIS_ID;
            if ((fit_fis_id_exists) and (item['fit_fis_id'] != None) and (item['fit_fis_id'] != '')):
                values = collect.to_dict()
                del values['id']

                smtp = update(Coleta).where(
                    Coleta.fit_fis_id == item['fit_fis_id']).values(values)
                [session.execute(smtp), session.close()]

                row_edited_count += 1
                continue

            try:
                row_added_count += 1
                [session.add(collect), session.commit()]

                if ((row_added_count % 10) == 0):
                    os.system('clear||cls')

                    print(
                        f'⌛ Foram adicionadas um total de {colored(f"{row_added_count}", "green")} linhas no banco de dados até agora;\nAguarde até o final da execução do programa;\n')
            except Exception as e:
                row_error_count += 1

                if ((row_error_count % 10) == 0):
                    print(
                        f'❌ Um erro foi encontrado ao tentar inserir uma linha no banco de dados;\nUm total de {colored(f"{row_error_count}", "red")} foram encontrados até agora.\nCausa do erro: {colored(f"{e.__cause__}", "red")}\n')

    print(
        f'✅ Um total de {colored(f"{row_added_count}", "green")} novas linhas foram adicionadas ao banco de dados;')
    print(
        f'♻️ Um total de {colored(f"{row_edited_count}", "blue")} linhas passaram por um update no banco de dados;')
    print(
        f'❌ Um total de {colored(f"{row_error_count}", "red")} erros ocorreram ao tentar inserir novos items.')


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

                                smtp = update(Coleta).where(
                                    Coleta.fit_fis_id == item['fit_fis_id']).values(values)
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
