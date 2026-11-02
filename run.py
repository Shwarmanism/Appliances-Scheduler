from sqlalchemy import inspect, text
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # create_all() never alters existing tables, so add columns introduced later.
        cols = {c['name'] for c in inspect(db.engine).get_columns('scheduled_appliances')}
        if 'selected_type' not in cols:
            with db.engine.begin() as conn:
                conn.execute(text("ALTER TABLE scheduled_appliances ADD COLUMN selected_type VARCHAR(3)"))
    app.run(debug=True, port=5001) 