
from data_generate import DataGenerator


#  get data
num_data = 1
num_elements = 10
max_depth = 3

data_generator = DataGenerator(num_elements=num_elements,  max_depth=max_depth)
datasets = [data_generator.generate_dataset() for _ in range(num_data)]

for i,dataset in enumerate(datasets):
    data_generator.save_tree_as_dot(dataset, f'{i}_generated_tree.dot')


# BTP inside and outside




# BTP with composition action