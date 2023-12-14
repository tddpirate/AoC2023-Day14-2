#!/usr/bin/env python
########################################################################
#
# day14_2.py
# Was written for AoC2023 by Omer Zak
#
########################################################################
import copy
from functools import cache
import re
import sys
from typing import Dict, List, Sequence, Set, TextIO, Tuple, Union

########################################################################
# Constants
########################################################################

# T = TypeVar("T")

########################################################################
# Functions
########################################################################


# 14_1 functions


def transpose(inpdata: Sequence[str]) -> List[str]:
    return list(map("".join, zip(*inpdata)))


@cache
def tilt_and_analyze(row: str) -> int:
    """
    Segment the row according to positions of '#'.
    Determine coordinates of '#'.
    Count number of 'O' in each segment.
    Compute its contribution to load.
    """
    splitted: List[str] = row.split("#")
    segmentlengths: List[int] = [len(segment) + 1 for segment in splitted]
    splitpositions: List[int] = [
        sum([seglen for seglen in segmentlengths[:segindex]])
        for segindex in range(len(segmentlengths))
    ]
    splitrocks: List[int] = [segment.count("O") for segment in splitted]
    sys.stdout.write(
        f"tilt_and_analyze: row={row}\n\tsegmentlengths={segmentlengths}\n\tsplitpositions={splitpositions}\n\tsplitrocks={splitrocks}\n"
    )

    # To compute load due to segment:
    #  startrow=(row_length - splitposition)
    row_length = len(row)
    sys.stdout.write(f"    row_length={row_length}\n")
    computeload = (
        lambda startrow, numrocks: (
            startrow * (startrow + 1)
            - (startrow - numrocks) * (startrow - numrocks + 1)
        )
        / 2
    )
    load_by_segment: List[int] = [
        computeload(row_length - splitpositions[segind], splitrocks[segind])
        for segind in range(len(splitted))
    ]
    sys.stdout.write(f"\tload_by_segment={load_by_segment}\n")
    return sum(load_by_segment)


def compute_total_load(inp_platform: Sequence[str]) -> int:
    """Compute load on north support beams"""
    platform_w: List[str] = transpose(inp_platform)
    return sum([tilt_and_analyze(row) for row in platform_w])


# 14_2 functions


def compute_total_load_2(inp_platform: Sequence[str]) -> int:
    """Compute load on north support beams, but without tilting the platform"""
    total_load = 0
    total_rows = len(inp_platform)
    for rind, row in enumerate(inp_platform):
        total_load += row.count("O") * (total_rows - rind)
    return total_load


@cache
def tilt_row(row: str) -> str:
    """Tilt row to the left."""
    splitted: List[str] = row.split("#")
    return "#".join(
        [
            "O" * segment.count("O") + "." * (len(segment) - segment.count("O"))
            for segment in splitted
        ]
    )


def one_cycle(inp_platform: Sequence[str]) -> Sequence[str]:
    # Tilt to the north
    platform_n: Sequence[str] = transpose(
        [tilt_row(row) for row in transpose(inp_platform)]
    )
    # Tilt to the west
    platform_w: Sequence[str] = [tilt_row(row) for row in platform_n]
    # Tilt to the south
    platform_s: Sequence[str] = transpose(
        [tilt_row(row[::-1])[::-1] for row in transpose(platform_w)]
    )
    # Tilt to the east
    platform_e: Sequence[str] = [tilt_row(row[::-1])[::-1] for row in platform_s]
    return platform_e


def print_platform(cycle: int, platform: Sequence[str]):
    for row in platform:
        sys.stdout.write(f"{cycle:12}: {row}\n")


########################################################################
# Patterns
########################################################################


########################################################################
# Classes for raising exceptions
########################################################################
class error(Exception):
    pass


class StopLoop(Exception):
    pass


if __name__ == "__main__":
    ########################################################################
    # Input data parsing
    ########################################################################

    platform: List[str] = []
    for line in sys.stdin:
        sline = line.strip()
        if len(sline) == 0:
            # Ignore empty lines, no special processing is needed.
            continue
        platform.append(sline)

    ########################################################################
    # Main loop
    ########################################################################

    # We want to stop after few memoizer hits.
    memoizer: Dict[Tuple[str, ...], int] = {tuple(platform): 0}
    memoizer_hit_count: int = 0

    print_platform(0, platform)
    sys.stdout.write(f"{0:12}: total load {compute_total_load_2(platform)}\n")

    sys.stdout.write("\n\n")

    for cycle in range(1, 1_000_000_001):
        new_platform: List[str] = list(one_cycle(platform))
        if new_platform == platform:
            sys.stdout.write("--- No further changes ---\n")
            break
        if cycle < 5:
            print_platform(cycle, new_platform)
        total_load: int = compute_total_load_2(new_platform)

        tuple_new_platform = tuple(new_platform)
        if tuple_new_platform in memoizer:
            cycle_length = cycle - memoizer[tuple_new_platform]

            remaining_cycles = 1_000_000_000 - cycle
            remaining_after_modulo = remaining_cycles % cycle_length
            sys.stdout.write(
                f"--- memoizer hit. current cycle {cycle}, previous was in cycle {memoizer[tuple_new_platform]}  cycle length={cycle_length} remaining:{remaining_cycles}  remaining after modulo={remaining_after_modulo}\n"
            )
            if remaining_after_modulo == 0:
                sys.stdout.write(f"\n>>> ANSWER: {total_load} <<<\n")
                break
            memoizer_hit_count += 1
            if memoizer_hit_count >= 10:
                sys.stdout.write("--- Enough memoizer hits, stopping ---\n")
                break
        memoizer[tuple_new_platform] = cycle

        platform = new_platform

        sys.stdout.write(f"{cycle:12}: total load {total_load}\n")

    ########################################################################
    # Write out answer
    ########################################################################

    # Already written above

else:
    pass

########################################################################
# End of day14_2.py
