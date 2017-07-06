days = ['Monday', 'Tuesday', 'Wednesday']
fruits = ['banana', 'orange', 'peach']
drinks = ['coffee', 'tea', 'beer']
desserts = ['tiramisu', 'ice cream', 'pie', 'pudding']

for days, fruits, drinks, desserts in zip(days, fruits, drinks, desserts):
    print(days, ": drink", drinks, "- eat", fruits, "- enjoy", desserts)

english = 'Monday', 'Tuesday', 'Wednesday'
french = 'Lundi', 'Mardi', 'Mercredi'

zip_list = list(zip(english, french))
print(zip_list)

zip_dict = dict(zip(english, french))
print(zip_dict)