import numpy as np
import helpers as h


np_array = np.random.random((30, 30))
h5_name = 'mnistmodel.h5'
h.write_dh5_np(h5_name, np_array)
np_array_from_h5 = h.read_hd5_np(h5_name)
np.allclose(np_array_from_h5, np_array)
txt_name = 'mnistmodel.txt'
txt_name = h.convert_to_txt(h5_name, txt_name)
np_array_from_txt = np.loadtxt(txt_name)
np.allclose(np_array_from_txt, np_array)