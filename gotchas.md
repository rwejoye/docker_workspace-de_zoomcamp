# Dependency Discovery: A Note on uv, pgcli, and Transitive Dependencies

The code works on my machine, but it highlighted a potential bottleneck for production. Here’s
why.
I’ve been diving into the Data Engineering Zoomcamp by Alexey Grigorev lately. While building
out a data pipeline script based on the real-world workflows introduced in the course, I imported
click to handle some CLI commands.
The script ran fine. But when I checked my pyproject.toml to review my project dependencies,
I noticed something odd: click wasn’t listed anywhere.
How was it importing successfully if I hadn’t explicitly added it?
I dug into the uv.lock file and found the answer: click was being pulled in as a transitive
dependency through pgcli .
To double-check this in isolation, I spun up a clean python:3.14-slim Docker container,
ran pip install pgcli , and checked pip show click . Sure enough, it was already there,
automatically installed through the dependency chain.
Why this matters:
Even though this setup works fine locally, relying on implicit, transitive dependencies poses a risk
for deployment.
For instance, if a deployment workflow uses a command like uv sync --no-dev to strip out
development tools like pgcli , the environment might not include click . That scenario could
introduce unexpected ModuleNotFoundError issues down the line.
Furthermore, there’s a risk with upstream packages (meaning the tools your project relies on,
like pgcli ). If the creators of pgcli ever update their codebase in the future and decide to drop
click entirely, your local pipeline could suddenly break without you ever changing a single line
of your own code.
I ran uv add click to make the configuration explicit and robust. Working code doesn’t
always mean an explicitly declared configuration. Tools like pyproject.toml , uv.lock , and
Docker isolation exist exactly to bring these hidden relationships to light so we can build more
reliable pipelines.
#DataEngineering #Python #Docker #DevOps #LearningInPublic