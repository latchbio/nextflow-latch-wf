FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:dd8f-main

RUN apt-get update -y && \
    apt-get install -y curl unzip git

# Install Nextflow
RUN apt-get install -y default-jre-headless 
RUN curl -s https://get.nextflow.io | bash && \
    mv nextflow /usr/bin/ && \
    chmod 777 /usr/bin/nextflow 

# Install micromamba
ENV CONDA_DIR /opt/conda
ENV MAMBA_ROOT_PREFIX /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN apt-get update && apt-get install -y wget bzip2 \
    && wget -qO-  https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba \
    && touch /root/.bashrc \
    && ./bin/micromamba shell init -s bash -p /opt/conda  \
    && grep -v '[ -z "\$PS1" ] && return' /root/.bashrc  > /opt/conda/bashrc   # this line has been modified \
    && apt-get clean autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

SHELL ["bash", "-l" ,"-c"]

# Copy the original rnaseq-nf workflow 
COPY rnaseq-nf /root/rnaseq-nf

# Install conda dependencies
RUN micromamba create -f /root/rnaseq-nf/conda.yml -y

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
RUN git clone https://github.com/latchbio/latch && cd latch && pip install -e .

COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
