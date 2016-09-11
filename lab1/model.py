import pickle


class Performer:
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.composition_list = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        for composition in self.composition_list:
            composition.performer = name

    def get_country(self):
        return self.country

    def set_country(self, country):
        self.country = country

    def get_composition_list(self):
        return self.composition_list

    def add_composition(self, title, duration, performer):
        self.composition_list.append(Composition(title, duration, performer))

    def find_composition(self, title):
        for composition in self.composition_list:
            if composition.title == title:
                return composition

    def remove_composition(self, title):
        for composition in self.composition_list:
            if composition.title == title:
                del composition
                break
        else:
            return False
        return True


class Composition:
    def __init__(self, title, duration, performer):
        self.title = title
        self.duration = duration
        self.performer = performer

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_duration(self, duration):
        self.duration = duration

    def get_duration(self):
        return self.duration

    def set_performer(self, performer):
        self.performer = performer

    def get_performer(self):
        return self.performer


class Database:

    # def __init__(self, first_essence_datafile, second_essence_datafile, pkl_filename):
    def __init__(self, pkl_filename):

        self.database_file = pkl_filename
        f = open(pkl_filename, 'rb')
        self.data_list = pickle.load(f)

        # for performer in open(first_essence_datafile, 'r'):
        #     name, country = performer.split(';')
        #     country = country.rstrip('\n')
        #     self.data_list.append(Performer(name, country))

        # i = 0
        # for composition in open(second_essence_datafile, 'r'):
        #     title, duration, performer = composition.split(';')
        #     performer = performer.rstrip('\n')
        #     if performer != self.data_list[i].name:
        #         i += 1
        #     self.data_list[i].composition_list.append(Composition(title, duration, performer))

    def add_performer(self, name, country):
        self.data_list.append(Performer(name, country))

    def find_performer(self, name):
        for performer in self.data_list:
            if performer.name == name:
                return performer

    def del_performer(self, name):
        search_res = self.find_performer(name)
        if search_res:
            self.data_list.remove(search_res)

    def performers_with_average_time_4(self):
        res = []
        for performer in self.data_list:
            sum_of_times = 0.0
            for composition in performer.composition_list:
                dur = float(composition.duration)
                sum_of_times += float(int(dur) * 60 +       # convert float format to seconds
                                      100 * (dur - int(dur))) / 60

            comp_list_len = len(performer.composition_list)
            if comp_list_len != 0 and sum_of_times / len(performer.composition_list) > 4:
                res.append(performer)

        return res

    def rewrite(self):
        f = open(self.database_file, 'wb')
        pickle.dump(self.data_list, f)
