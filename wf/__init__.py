"""
A basic pipeline for quantification of genomic features from short read data implemented with Nextflow and wrapped inside the Latch SDK.
"""

import subprocess
from pathlib import Path
from typing import List
from latch import medium_task, workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchAuthor, LatchFile, LatchMetadata, LatchParameter, LatchDir


@medium_task
def rnaseq_task(
    reads: List[LatchFile] = [
        LatchFile("s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_gut_1.fq"),
        LatchFile("s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_gut_2.fq"),
    ],
    transcriptome: LatchFile = LatchFile(
        "s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_1_48850000_49020000.Ggal71.500bpflank.fa"
    ),
    outdir: LatchDir = LatchDir("latch:///rnaseq-nf/results"),
) -> LatchDir:

    local_outputdir = outdir.local_path
    print(local_outputdir)
    subprocess.run(["ls", local_outputdir])

    Path(reads[0].local_path).rename("/root/read_1.fq")
    Path(reads[1].local_path).rename("/root/read_2.fq")

    files = "/root/read_{1,2}.fq"

    nf_cmd = [
        "/root/bin/micromamba",
        "run",
        "-n",
        "rnaseq-nf",
        "/bin/bash",
        "-c",
        f"""
        nextflow run /root/rnaseq-nf/main.nf \
        -profile conda \
        --reads '{files}' \
        --transcriptome {transcriptome.local_path} \
        """,
    ]

    subprocess.run(nf_cmd, check=True)

    return LatchDir("/root/results", outdir.remote_path)


"""The metadata included here will be injected into your interface."""
metadata = LatchMetadata(
    display_name="Porting RNAseq-NF pipeline to Latch SDK",
    documentation="https://github.com/latchbio/nextflow-latch-wf",
    author=LatchAuthor(
        name="Hannah Le",
        email="hannah@latch.bio",
        github="https://github.com/latchbio/nextflow-latch-wf",
    ),
    repository="https://github.com/latchbio/nextflow-latch-wf",
    license="MIT",
    parameters={
        "reads": LatchParameter(
            display_name="Forward and Reverse reads",
            description="Paired-end read 1 and 2 files to be aligned.",
        ),
        "transcriptome": LatchParameter(
            display_name="Transcriptome", description="Select transcriptome (.fa)"
        ),
        "outdir": LatchParameter(
            display_name="Output Directory", description="Select output directory."
        ),
    },
    tags=[],
)


@workflow(metadata)
def rnaseq_wf(
    reads: List[LatchFile], transcriptome: LatchFile, outdir: LatchDir
) -> LatchDir:
    """Description...

    markdown header
    ----

    Write some documentation about your workflow in
    markdown here:

    > Regular markdown constructs work as expected.

    # Heading

    * content1
    * content2
    """
    return rnaseq_task(reads=reads, transcriptome=transcriptome, outdir=outdir)


"""
Add test data with a LaunchPlan. Provide default values in a dictionary with
the parameter names as the keys. These default values will be available under
the 'Test Data' dropdown at console.latch.bio.
"""
LaunchPlan(
    rnaseq_wf,
    "Test Data",
    {
        "reads": [
            LatchFile(
                "s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_gut_1.fq"
            ),
            LatchFile(
                "s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_gut_2.fq"
            ),
        ],
        "transcriptome": LatchFile(
            "s3://latch-public/test-data/6064/rnaseq-nf/data/ggal/ggal_1_48850000_49020000.Ggal71.500bpflank.fa"
        ),
        "outdir": LatchDir("latch:///welcome"),
    },
)
