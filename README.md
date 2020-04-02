# shushi ­ƒìñ
Minimalist secrets management in Python for Windows.

## Requirements
- Python 3.7.*

## Installation
```posh
> pip install shushi
```

## CLI Usage
Create a vault:
```posh
> shushi -p [password] make
```

Open a cli form to add an item to your vault:
```posh
> shushi -p [password] add [name]
```

Retrieve an item from your vault:
```posh
> shushi -p [password] get [name]
```

Remove an item from your vault:
```posh
> shushi -p [password] remove [name]
```

List all items in your vault:
```posh
> shushi -p [password] list
```

## Advanced CLI Usage
Shushi can read your password from an Environment Variable `SHUSHI_PASSWORD`.

Set your vault password Environment Variable:
```posh
> Set-Item -Path Env:SHUSHI_PASSWORD -Value "[password]"
```

This removes the need to use the `-p/--password` option when calling shushi commands.

Before:
```posh
> shushi -p [password] get [name]
```

After:
```posh
> shushi get [name]
```