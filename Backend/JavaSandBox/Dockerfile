# Use an official OpenJDK base image with a specific version that includes the JDK
FROM openjdk:11

# Set the working directory inside the container
WORKDIR /app

# Copy the Java sandbox code to the container's working directory
COPY java_sandbox /app/java_sandbox

# Expose the port that the Java sandbox will listen on (if applicable)
# For example, if your Java sandbox runs a server on port 8080, you can expose it as follows:
EXPOSE 8080

# Define the command to start the Java sandbox application
# For example, if your Java sandbox is a JAR file, you can run it with the following command:
CMD ["java", "-jar", "/app/java_sandbox/your-java-sandbox.jar"]