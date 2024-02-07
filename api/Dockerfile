FROM gradle:8.5-jdk17-jammy as build

WORKDIR /app

COPY gradle gradle
COPY gradlew .
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY src src

RUN --mount=type=cache,target=/root/.gradle gradle bootJar --parallel
RUN cp build/libs/*.jar /app.jar

EXPOSE 8080

FROM eclipse-temurin:17-jdk-alpine as development
COPY --from=build /app.jar /app.jar
ENTRYPOINT ["java", "-Dspring-boot.repackage.excludeDevtools=false", "-Dspring-boot.run.jvmArguments='-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000'","-Dspring.profiles.active=dev","-jar","/app.jar"]

FROM eclipse-temurin:17-jdk-alpine as production
COPY --from=build /app.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-Dspring.profiles.active=prod","-jar","/app.jar"]