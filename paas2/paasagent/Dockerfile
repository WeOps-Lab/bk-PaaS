FROM golang as builder
RUN go env -w GOPROXY=https://goproxy.cn

WORKDIR /apps
COPY . .
RUN make build

FROM centos:7
WORKDIR /opt
COPY --from=builder /apps/bin/paas_agent /opt/paas_agent/paas_agent/bin/
COPY --from=builder /apps/etc /opt/paas_agent/paas_agent/etc
COPY --from=builder /apps/support-files /opt/paas_agent/support-files
COPY --from=builder /apps/VERSION /opt/paas_agent/VERSION
COPY --from=builder /apps/README.md /opt/paas_agent/README.md
COPY --from=builder /apps/projects.yaml /opt/paas_agent/projects.yaml
WORKDIR /opt/paas_agent