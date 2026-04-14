# Reference GDS generation for XOR validation against Magic.
#
# Builds Magic VLSI + open_pdks GF180MCU at PINNED commits.
# The committed ref_gds/ files were generated from exactly these versions.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# ── Pinned upstream commits ──────────────────────────────────────────────
ARG MAGIC_COMMIT=67c6ed939514e537773f9f01cc2ecca5c3400c44
ARG OPEN_PDKS_COMMIT=fc20c144baf309002e0b335585a3aaef06b56f00
# ─────────────────────────────────────────────────────────────────────────

RUN apt-get update && apt-get install -y \
    build-essential git python3 tcl-dev tk-dev \
    libcairo2-dev libx11-dev libxpm-dev libglu1-mesa-dev \
    m4 csh \
    && rm -rf /var/lib/apt/lists/*

# Build Magic
RUN git clone https://github.com/RTimothyEdwards/magic.git /tmp/magic && \
    cd /tmp/magic && git checkout ${MAGIC_COMMIT} && \
    ./configure && make -j$(nproc) && make install && \
    rm -rf /tmp/magic

# Build open_pdks — GF180MCU only
RUN git clone https://github.com/RTimothyEdwards/open_pdks.git /tmp/open_pdks && \
    cd /tmp/open_pdks && git checkout ${OPEN_PDKS_COMMIT} && \
    ./configure --enable-gf180mcu-pdk --with-gf180mcu-variants=A && \
    make -j$(nproc) && make install && \
    rm -rf /tmp/open_pdks

RUN echo 'puts "Magic OK"; quit -noprompt' | magic -dnull -noconsole

WORKDIR /work
COPY sweep_params.json /work/sweep_params.json
COPY generate_references.sh /work/generate_references.sh
RUN chmod +x /work/generate_references.sh

ENV REF_DIR=/output
ENTRYPOINT ["/work/generate_references.sh"]
