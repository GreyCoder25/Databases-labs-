import model
import view

db = model.Database('database.pkl')

while True:
    query = view.start_menu()

    if query == 1:
        search_res = db.find_performer(view.search_or_del())
        if search_res:
            view.print_performer(search_res)
        else:
            view.failed_search('Performer')
    elif query == 2:
        name, country = view.add_performer()
        db.add_performer(name, country)
        db.rewrite()
    elif query == 3:
        edit_query = view.edit()

        if edit_query == 1:
            edit_performer_query = view.edit_performer()
            search_res = db.find_performer(view.search_or_del())
            if search_res:
                if edit_performer_query == 1:
                    search_res.set_name(view.new_value())
                elif edit_performer_query == 2:
                    search_res.set_country(view.new_value())
            else:
                view.failed_search('Performer')
        elif edit_query == 2:
            title, duration = view.add_composition()
            perf_name = view.search_or_del()
            search_res = db.find_performer(perf_name)
            if search_res:
                search_res.add_composition(title, duration, perf_name)
            else:
                view.failed_search('Performer')
        elif edit_query == 3:
            edit_composition_query = view.edit_composition()
            search_res = db.find_performer(view.search_or_del())
            if search_res:
                composition = search_res.find_composition(view.search_or_del_compos())
                if composition:
                    if edit_composition_query == 1:
                        composition.set_title(view.new_value())
                    elif edit_composition_query == 2:
                        composition.set_duration(view.new_value())
                else:
                    view.failed_search('Composition')
            else:
                view.failed_search('Performer')
        db.rewrite()
    elif query == 4:
        view.print_special(db.performers_with_average_time_4())
    elif query == 5:
        view.print_data(db)
    elif query == 6:
        db.del_performer(view.search_or_del())
        db.rewrite()
    elif query == 7:
        break
