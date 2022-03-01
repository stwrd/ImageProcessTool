import numpy as np
import torch
import torchvision.datasets
from pathlib import Path
import pandas as pd

def load_data():
    # passengers number of international airline , 1949-01 ~ 1960-12 per month
    seq_number = np.array(
        [112., 118., 132., 129., 121., 135., 148., 148., 136., 119., 104.,
         118., 115., 126., 141., 135., 125., 149., 170., 170., 158., 133.,
         114., 140., 145., 150., 178., 163., 172., 178., 199., 199., 184.,
         162., 146., 166., 171., 180., 193., 181., 183., 218., 230., 242.,
         209., 191., 172., 194., 196., 196., 236., 235., 229., 243., 264.,
         272., 237., 211., 180., 201., 204., 188., 235., 227., 234., 264.,
         302., 293., 259., 229., 203., 229., 242., 233., 267., 269., 270.,
         315., 364., 347., 312., 274., 237., 278., 284., 277., 317., 313.,
         318., 374., 413., 405., 355., 306., 271., 306., 315., 301., 356.,
         348., 355., 422., 465., 467., 404., 347., 305., 336., 340., 318.,
         362., 348., 363., 435., 491., 505., 404., 359., 310., 337., 360.,
         342., 406., 396., 420., 472., 548., 559., 463., 407., 362., 405.,
         417., 391., 419., 461., 472., 535., 622., 606., 508., 461., 390.,
         432.], dtype=np.float32)
    # assert seq_number.shape == (144, )
    # plt.plot(seq_number)
    # plt.ion()
    # plt.pause(1)
    seq_number = seq_number[:, np.newaxis]

    # print(repr(seq))
    # 1949~1960, 12 years, 12*12==144 month
    seq_year = np.arange(12)
    seq_month = np.arange(12)
    seq_year_month = np.transpose(
        [np.repeat(seq_year, len(seq_month)),
         np.tile(seq_month, len(seq_year))],
    )  # Cartesian Product

    seq = np.concatenate((seq_number, seq_year_month), axis=1)

    # normalization
    seq = (seq - seq.mean(axis=0)) / seq.std(axis=0)
    return seq

def create_dataset(data_path):
    total_file = Path(data_path).rglob('*.jpg')
    sample_interval = 10
    sample_length = 10
    for file in total_file:
        sequence = pd.read_csv(file)
        rows,cols = sequence.shape
        for start in range(0,rows-sample_length,sample_interval):
            single_sample = sequence[start:start+sample_interval]

            factor_close = single_sample['close'][:sample_length//2]
            factor_high = single_sample['high'][:sample_length//2]
            factor_open = single_sample['open'][:sample_length//2]
            factor_low = single_sample['low'][:sample_length//2]
            factor_volume = single_sample['volume'][:sample_length//2]

            factor_high_low = factor_high - factor_low
            factor_high_low.fillna(0)
            factor_open_close = factor_close - factor_open
            factor_open_close.fillna(0)
            factor_close_diff = factor_close - factor_close.shift(1)
            factor_close_diff.fillna(0)
            factor_high_diff = factor_high - factor_high.shift(1)
            factor_high_diff.fillna(0)
            factor_open_diff = factor_open - factor_open.shift(1)
            factor_open_diff.fillna(0)
            factor_low_diff = factor_low - factor_low.shift(1)
            factor_low_diff.fillna(0)
            factor_volume_change_rate = (factor_volume - factor_volume.shift(1))/factor_volume
            factor_volume_change_rate.fillna(1.0)

            #future label
            future_high = single_sample[sample_length//2:]['high'].max()
            future_low = single_sample[sample_length//2:]['low'].min()






if __name__ == '__main__':
    seq_len = 48
    batch_size = 1
    inp_dim = 3
    mid_dim = 20
    rnn = torch.nn.LSTM(3, 20, 2)
    input = torch.randn(seq_len, batch_size, inp_dim)
    output,(hn,cn) = rnn(input)
    assert output.size() == (seq_len, batch_size, mid_dim)
    rnn = torch.nn.LSTM(10,20,3)
    input = torch.randn(5,1,10)
    h0 = torch.randn(3,1,20)
    c0 = torch.randn(3,1,20)
    output,(hn,cn) = rnn(input,(h0,c0))
    print(output)