from hashlib import new
from app import *
from sqlalchemy.sql import text


if __name__ == "__main__":
    date = f'{datetime.now().day - 1}/{datetime.now().month:02d}/{datetime.now().year}'

    request = RequestExpress(
        'qi7nsdzyTU3FRo1MA5MYLFgboVLPz9tHShybLesgUeA-Q5rxwytAWw'
    )
    response = request.get_template_from_date(date)

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
