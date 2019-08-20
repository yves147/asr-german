import datetime
import argparse
import functools
from utils.utility import add_arguments, print_arguments
import os

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('input_file', str,
        '',
        "The default title from the text in dataset"
        )
add_arg('output_file', str,
        '',
        "The output file you want to place."
        )
add_arg('infer_manifest', str,
        'data/aishell/manifest.test',
        "Filepath of manifest to infer.")
args = parser.parse_args()


def infer():
    with open(args.input_file, 'r') as f:
        l = f.readlines()
        l[8] = "ASR_02|DE\n"
        start_time = l[10].split('|')[0]
        end_time = l[10].split('|')[1]
        time_now = str(datetime.datetime.now())[:16]  # get the current time
        l[10] = "|".join(["ASR_02", time_now, "Source_Program=Kaldi,infer.sh", "Source_Person=Aashish Agarwal",
                          "Codebook=Deutsch Speech to Text\n"])
        end_line = ""
        if l[-1].startswith("END"):
            end_line = l[-1]
        l = l[:11]
        curpath = os.path.abspath(os.curdir)
        print(curpath)
        print(l)

    with open(args.output_file, "w") as f:
        f.writelines(l)

    with open(args.infer_manifest, "r") as input_file:
        with open(args.output_file, 'a+') as f:
            transcript=input_file.read()
            #print("\nOutput Transcription: %s" %transcript.encode('utf-8'))
            print(start_time)
            start, m_sec = start_time.split('.')
            time_format = '%Y%m%d%H%M%S'
            end = (datetime.datetime.strptime(start, time_format) + datetime.timedelta(0, 10)).strftime(time_format)
            prefix = start + '.' + m_sec + '|' + end + '.' + m_sec + '|ASR_02|'
            f.write(prefix)
            #f.write(transcript.encode('utf-8'))
	    f.write(transcript)
            f.write('\n')

    with open(args.output_file, 'a+') as f:
        f.write(end_line)


def main():
    print_arguments(args)
    infer()


if __name__ == '__main__':
    main()