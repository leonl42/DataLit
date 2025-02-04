import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from parse import parse,find_main_tex
import argparse
from timeit import default_timer as timer

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process and analyze LaTeX files.")

    parser.add_argument(
        '--tex-path', type=str, help="Path to the LaTeX source files."
    )

    parser.add_argument(
        '--save-path', type=str, help="Path to save processed files."
    )

    parser.add_argument(
        '--mem-limit', type=int, default=2500, help="Memory limit in megabytes (default: 2.5GB)."
    )

    parser.add_argument(
        '--timeout', type=int, default=10, help="Timeout in seconds for processing."
    )

    parser.add_argument(
        '--num-workers', type=int, default=6, help="Number of worker threads to use."
    )

    parser.add_argument('--skip-existing', action='store_true', default=False, help="Skip processing of already parsed files."
    )

    parser.add_argument('--skip-failed', action='store_true', default=False, help="Skip processing of already files that failed parsing."
    )

    parser.add_argument('--print-stats', action='store_true', default=False, help="Print statistics during processing."
    )


    args = parser.parse_args()

    list_args = []

    for folder in os.listdir(args.tex_path):
        if os.path.isdir(os.path.join(args.tex_path,folder)):
            list_args.append([os.path.join(args.tex_path,folder),os.path.join(args.save_path,folder)])

    def _parse(e):
        (tex_path,save_path) = e
        os.makedirs(save_path,exist_ok=True)

        # Skip if was already parsed
        if args.skip_existing and os.path.exists(os.path.join(save_path,"parsed.math")):
            return
        
        # Skip if parsing failed
        if args.skip_failed and os.path.exists(os.path.join(save_path,"failed.error")):
            return
        
        # Try to identify the .tex file for parsing
        main_tex = find_main_tex(tex_path)
        
        if main_tex:
            start_parsing = timer()
            result = parse(tex_path,save_path,main_tex,args.mem_limit*1024*1024,args.timeout)
            end_parsing = timer()

            if args.print_stats:
                conversion_rate = [int(os.path.exists(os.path.join(args.save_path,folder,"parsed.math"))) for folder in os.listdir(args.tex_path)
                                            if os.path.exists(os.path.join(args.save_path,folder,"parsed.math")) or os.path.exists(os.path.join(args.save_path,folder,"failed.error"))]
                conversion_rate = round(100*sum(conversion_rate)/len(conversion_rate), 2)


                done_rate = [os.path.exists(os.path.join(args.save_path,folder,"parsed.math")) or os.path.exists(os.path.join(args.save_path,folder,"failed.error")) 
                             for folder in os.listdir(args.tex_path)]
                done_rate = round(100*sum(done_rate)/len(done_rate),2)

                print("{0} | Took: {1}s | Conversion rate: {2}% | Done: {3}%".format(result, round(end_parsing-start_parsing,4), conversion_rate, done_rate))


    with multiprocessing.Pool(processes=args.num_workers) as pool:
        pool.map(_parse,list_args)

