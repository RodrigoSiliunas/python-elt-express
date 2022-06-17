from msilib.schema import Error
from time import sleep
from termcolor import colored
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.packages import RequestExpress, MailExpress
from app.database.models import Coleta, DeclarativeBase

from app.configurations import DevelopmentConfig

engine = create_engine(DevelopmentConfig.DATABASE_URI)


def init_db():
    DeclarativeBase.Model.metadata.create_all(bind=engine)


def insert_data_on_table(sleep_time: int = 1):
    mail = MailExpress(
        'smtp.mailtrap.io',
        2525,
        'e46dc7ab483db9',
        '66f0eabf5ff39d'
    )

    while True:
        if (datetime.now().hour == 17):
            try:
                date = f'{datetime.now().day}/{datetime.now().month:02d}/{datetime.now().year}'

                print(
                    f'⚠️ {colored("ATENÇÃO:", "red")} Início do processo de atualização do banco de dados.\n'
                    f'Fazendo a requisição ao {colored("ESL", "blue")} dos dados da data atual: {colored(date, "green")}.\n'
                )

                request = RequestExpress(
                    'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw'
                )
                response = request.get_template_from_date(date, date).json()

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
                            esl_id = item['id']
                            item['esl_id'] = esl_id
                            del item['id']


                            collect = Coleta(**item)

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

        # The process will sleep after verify if is the hour of the insertion.
        sleep(sleep_time * 60 * 60)
