from transformers import AutoTokenizer, BertTokenizer

from fairseq.models import FairseqEncoderDecoderModel

# parser = options.get_interactive_generation_parser()
# parser.batch_size = 1
# args = options.parse_args_and_arch(parser)
#
# cfg = convert_namespace_to_omegaconf(args)


# task = tasks.setup_task(cfg.task)
# TestModel.build_model(args, self)

de2en = FairseqEncoderDecoderModel.from_pretrained(
    './model/',
    checkpoint_file='checkpoint_best.pt',
    # data_name_or_path='data-bin/wmt17_zh_en_full',
    # bpe='bert',
    # pretrained_bpe='./download_prepare/12k-vocab-models/',
    # pretrained_bpe_src='jhu-clsp/bibert-ende',
    vocab_file='./download_prepare/data_mixed_ft/de-en-databin/dict.en.txt'
)
src = '"Comfortable", danke.'

pretrained_lm = 'jhu-clsp/bibert-ende'
try:
    tokenizer = AutoTokenizer.from_pretrained(pretrained_lm)
except:
    tokenizer = BertTokenizer.from_pretrained(pretrained_lm)

# src = src.strip()
# toks = tokenizer.tokenize(src)
# toks = " ".join(toks)
#
# print('[TOKs]', toks)
#
# result = de2en.translate(toks)
#
# print(result)


# DATAPATH=./download_prepare/data_mixed_ft/
# STPATH=${DATAPATH}de-en-databin/
# MODELPATH=./models/dual-ft/
# PRE_SRC=jhu-clsp/bibert-ende
# PRE=./download_prepare/12k-vocab-models/
# CUDA_VISIBLE_DEVICES=0 fairseq-generate \
# ${STPATH} --path ${MODELPATH}checkpoint_best.pt --bpe bert --pretrained_bpe ${PRE} --pretrained_bpe_src ${PRE_SRC} \
# --beam 4 --lenpen 0.6 --remove-bpe --vocab_file=${STPATH}/dict.en.txt \
# --max-len-a 1 --max-len-b 50|tee ${STPATH}/generate-dual-fine.out

import re
def untokenize(text):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    # text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip().capitalize()

def translate(src):
  psrc = src.strip()
  toks = tokenizer.tokenize(psrc)
  toks = " ".join(toks)
  # print('[TOKs]', toks)
  pred = de2en.translate(toks)
  # result = tokenizer.decode(pred)
  result = untokenize(pred)
  return result

if __name__ == '__main__':
  while True:
    src = input(">> ")
    print(translate(src))