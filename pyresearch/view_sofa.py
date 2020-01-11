#! /usr/bin/env python
# coding: utf-8

import argparse
import json

import numpy as np
from SOFASonix import SOFAFile


# from modules.wave_handler_multi_ch import WaveHandler


def main():
    parser = argparse.ArgumentParser(description="This script shows information of *.sofa file.")

    parser.add_argument('sofa_path',
                        action='store',
                        nargs=None,
                        const=None,
                        default=None,
                        type=str,
                        help='Directory path where the *.sofa file is located.',
                        metavar=None)
    args = parser.parse_args()

    loadsofa = SOFAFile.load(args.sofa_path)

    # View the convention parameters
    loadsofa.view()

    # Copy impulse response data
    data = loadsofa.data_ir
    arr = np.array(data)
    print(arr.shape)

    print(loadsofa.SourcePosition)
    # for i in loadsofa.SourcePosition:
    #     print(i)
    print(loadsofa.getParam("ListenerPosition"))

    main_dic = {}
    params = loadsofa.flatten()
    for i in params:
        pi = params[i]
        value = pi.value.shape if \
            (pi.isType("double") or pi.isType("string")) else pi.value

        dic = {"shorthand": str(pi.getShorthandName()), "type": pi.type[0].upper(), "value": value,
               "ro": pi.isReadOnly(), "m": pi.isRequired(), "dims": pi.dimensions if pi.dimensions else None}

        main_dic[str(pi.getShorthandName())] = dic

    input_name_list = args.sofa_path.split("/")[-1].split(".")
    print(input_name_list)
    out_name = "".join(input_name_list[:-1]) + ".json"

    with open(f"/tmp/{out_name}", 'w') as f:
        # json.dump(main_dic, f, indent=4)
        json.dump(main_dic, f)

    # def view(self):
    #     cols = ["Shorthand", "Type", "Value", "RO", "M", "Dims"]
    #     rows = []
    #     params = self.flatten()
    #     for i in params:
    #         pi = params[i]
    #         value = "{} Array".format(pi.value.shape) if \
    #             (pi.isType("double") or pi.isType("string")) else pi.value
    #         rows.append([".{}".format(pi.getShorthandName()),
    #                      pi.type[0].upper(),
    #                      value,
    #                      pi.isReadOnly(),
    #                      pi.isRequired(),
    #                      str(pi.dimensions) if pi.dimensions else "_"])
    #     pd.set_option('display.max_colwidth', 40)
    #     pd.set_option('display.expand_frame_repr', False)
    #
    #     df = pd.DataFrame(rows, columns=cols)
    #     print(df)

    # Edit parameters
    # loadsofa.global_comment = "This is a new description of the file"
    #
    # Re-export sofa file
    # loadsofa.export("sofafile_new")


if __name__ == '__main__':
    main()
