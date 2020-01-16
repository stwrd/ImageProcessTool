import numpy as np

p = 0.8
sample_num = 10000
sample = np.random.random_sample(sample_num)
sample[sample>p] = 1
sample[sample<=p] = 0
print('sample ',sample.sum())

select = np.random.randint(0,2,sample_num)
print('select ',select.sum())

mask = (sample==select)
print(mask.astype('int32').sum())


a = [[1,2,3],[4,5,6],[7,8,9]]