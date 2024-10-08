# WoW Realmlist Manager

![image](https://github.com/user-attachments/assets/ca62b4f1-8fa3-4ead-8cce-6f608eadd031)

## Introduction

WoW Realmlist Manager is a tool designed to simplify the management of World of Warcraft (WoW) server configurations. It allows you to easily switch between multiple private servers across different versions of WoW, including Vanilla, The Burning Crusade, Wrath of the Lich King, and Cataclysm. With this application, you can manage server addresses, set realmlist paths, and launch WoW with the appropriate settings.

## Purpose

The purpose of this app is to make it easier to modify and manage the `realmlist.wtf` file, switch between multiple server addresses, and handle different WoW versions automatically. It is ideal for players who frequently switch between private servers.

## Features

- Add, edit, and delete server configurations.
- Automatically update the `realmlist.wtf` file for multiple WoW versions.
- Support for Vanilla (1.12.x), TBC (2.4.3), WotLK (3.3.5), and Cataclysm (4.3.4).
- Run WoW directly from the app after setting the configuration.

## Installation

1. **Prerequisites**:
    - Ensure you have Python 3.x installed on your machine. You can download it from [here](https://www.python.org/downloads/).

2. **Clone the repository**:
    ```bash
    git clone https://github.com/i-am-fyre/RealmlistManager.git
    ```

3. **Navigate to the project directory**:
    ```bash
    cd RealmlistManager
    ```

## Running the Application

1. **After cloning the repository, you can run the app by executing the following command**:
    ```bash
    python main.py
    ```

2. **Once the app is running**:

- Add a configuration by specifying the server name, realmlist.wtf path, WoW executable path, and server address.
- Select the version of WoW from the dropdown (Vanilla, TBC, WotLK, Cataclysm).
- Click Run WoW to launch the game with the specified configuration.

## Usage

- Add Configuration: Enter server details and click Add to save the configuration.
- Edit Configuration: Select a configuration, click Update, and modify the fields before saving.
- Delete Configuration: Select a configuration and click Delete to remove it.
- Run WoW: Select a configuration and click Run WoW to launch the game with the chosen settings.

## Contributing

Contributions are welcome! Feel free to open issues and pull requests on the [GitHub repository](https://github.com/i-am-fyre/RealmlistManager).

Thank you to [@fly-man-](https://github.com/fly-man-) for the additional support around `set portal`.

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/i-am-fyre/RealmlistManager/blob/master/LICENSE) file for more details.
