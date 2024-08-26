## Access the application inside a devcontainer

### 1. Open the Project in VS Code

* Open VSCode.
* Use the `File -> Open Folder...` menu to navigate to the directory where your project is located and open it.

### 2. Open the DevContainer

* Look at the bottom left corner of the VSCode window.
* Click on the green icon in the bottom-left corner (it typically says `><` or `Remote`).
* From the dropdown menu, select "Remote-Containers: Reopen in Container."
* VSCode will now reopen the project inside a Docker container defined by the `.devcontainer` configuration.

### 3. Wait for the Container to Build

* The first time you do this, VSCode will build the Docker container based on the Dockerfile specified in the `context = '..'`.

## Closing the DevContainer

* **Stopping the Container**: When you’re done working, you can close the VSCode window or use the green bottom-left corner to disconnect from the container by selecting "Remote-Containers: Close Remote Connection".
* **Reopening the Project Locally**: To reopen the project outside of the container, just close the current window and reopen the project in VSCode normally.


## Demo

![Demo](/static/images/accessing_devcontainer.gif)