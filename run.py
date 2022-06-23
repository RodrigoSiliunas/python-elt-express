from app import *
from sqlalchemy import exc, update


if __name__ == "__main__":
    init_db()
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

        print(
            f'✔️ {colored("SUCESSO:", "green")} O banco de dados foi atualizado com sucesso.\n'
            f'Um email informativo foi disparado ao operador. Próxima atualização no mesmo horário amanhã.\n'
        )
    except Exception as e:
        print(e)
    # insert_data_on_table()
