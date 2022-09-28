FROM nginx:latest
RUN apt-get update && apt-get install -y procps
RUN mkdir -p /home/app/staticfiles
RUN mkdir -p /home/app/mediafiles
# RUN mkdir -p /home/app/reactfiles

# COPY --from=build-stage /app/build/ /usr/share/nginx/html
# RUN mkdir -p /home/app/reactfiles
# ADD ./react/build/* /home/app/reactfiles/