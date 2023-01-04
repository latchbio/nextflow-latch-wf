from latch.types import LatchFile, LatchDir
from wf import rnaseq_task

rnaseq_task(
    reads=[
        LatchFile("s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_gut_1.fq"),
        LatchFile("s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_gut_2.fq"),
    ],
    transcriptome=LatchFile(
        "s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_1_48850000_49020000.Ggal71.500bpflank.fa"
    ),
    outdir=LatchDir("latch:///rnaseq-nf/results"),
)
