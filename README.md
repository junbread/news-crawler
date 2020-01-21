# news-crawler

Korean news dataset generator for building the NLP dataset. The generated file can be used in [pointer-generator](https://github.com/abisee/pointer-generator) project by Abigail See. Please refer this: [Get To The Point: Summarization with Pointer-Generator Networks](https://arxiv.org/abs/1704.04368)

This is a sub-project of [skku-coop-project](https://github.com/JunBread/skku-coop-project).

## Requirements

To run this, you should first install prerequisites. you can install them by run command below:

```bash
pip install requests koalanlp hanja beautifulsoup4 textrankr tensorflow
```

Also, you need to install `khaiii`. Please refer to [this instruction](https://github.com/kakao/khaiii/wiki/%EB%B9%8C%EB%93%9C-%EB%B0%8F-%EC%84%A4%EC%B9%98). `khaiii` supports only Linux environments.

## Usage

First, you need to gather raw news data from [BigKinds](https://www.bigkinds.or.kr) service. you can adjust parameters in `data`  to gather news from other categories. Default: 'society news'.

```bash
python crawler.py <article_size> <save_path>
```

> Note: BigKinds limits client requests strictly. They might block your IP after doing this job. Please use carefully.

Next, you need to process raw news data into regularized text and generate summaries. To do this, run command below:

```bash
python preprocessor.py <load_path> <save_path>
```

This may take a long time. After this, you can find processed articles in `.story` format under `save_path`. The files are plain text files. You can open them using a text editor.

To generate binary datasets which work with the pointer-generator project, type command below:

```bash
python dataset-processor.py <load_path>
```

> Note: `dataset-processor.py` file is originally not written by me. Please refer [this file](https://github.com/abisee/cnn-dailymail/blob/master/make_datafiles.py).

`load_path` is the location of preprocessed files, which is the output of `preprocessor.py`.

After this, you can find the `finished_files` directory under your working directory. This directory contains necessary files used by the pointer-generator project. You can test the dataset by [the project's instructions](https://github.com/abisee/pointer-generator#how-to-run).
