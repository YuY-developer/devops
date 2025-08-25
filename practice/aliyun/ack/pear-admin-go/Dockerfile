# 第一阶段：构建 Go 项目
FROM golang:1.24-alpine AS builder

WORKDIR /app

COPY . .

RUN go mod tidy && go build -o /app/app-binary /app/main.go

# 第二阶段：运行
FROM alpine:3.19   

WORKDIR /app

COPY --from=builder /app/app-binary /app/app

COPY config.toml /app/config.toml

EXPOSE 8009


