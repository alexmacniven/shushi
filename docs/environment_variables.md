# Environment Variables
Shushi can be configured using the environment variables of your host.

This document outlines the environment variables you can specify to alter the behaviour of both the CLI application and the API.


| Variable        | Description                  | Default                   | CLI | API |
|-----------------|------------------------------|---------------------------|-----|-----|
| SHUSHI_DATA     | The location of your vault.  | ~/AppData/Roaming/Shushi/ |  Y  |  Y  |
| SHUSHI_PASSWORD | The password for your vault. |                           |  Y  |  N  |

## SHUSHI_PASSWORD
This section details the usage of `SHUSHI_PASSWORD`.  
When using the Shushi CLI you can alleviate the need for supplying a password with every command by setting the environment variable.

Setting;
```posh
> Set-Item -Path Env:SHUSHI_PASSWORD -Value "my_password"
```
Turns this;
```posh
> shushi -p my_password get twitter
```
Into this;
```posh
> shushi get twitter
```