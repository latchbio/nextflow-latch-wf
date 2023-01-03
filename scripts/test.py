from latch.types import LatchFile, LatchDir
from wf import rnaseq_task

rnaseq_task(
    reads=[
        LatchFile("latch:///rnaseq-nf/ggal_gut_1.fq"),
        LatchFile("latch:///rnaseq-nf/ggal_gut_2.fq"),
    ],
    transcriptome=LatchFile(
        "latch:///rnaseq-nf/ggal_1_48850000_49020000.Ggal71.500bpflank.fa"
    ),
    outdir=LatchDir("latch:///rnaseq-nf/results"),
)