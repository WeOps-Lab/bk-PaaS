FROM golang as builder
RUN go env -w GOPROXY=https://goproxy.cn

WORKDIR /apps
ADD ./paas2 .

WORKDIR /apps/paasagent
RUN make build

FROM centos:7
COPY --from=builder /apps/paasagent/bin/paas_agent /app/paas_agent/paas_agent/bin/
COPY --from=builder /apps/paasagent/etc /app/paas_agent/paas_agent/etc
COPY --from=builder /apps/paasagent/support-files /app/paas_agent/support-files

WORKDIR /app/paas_agent