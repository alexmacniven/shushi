# shushi 🍤
Minimalist secrets management in Python for Windows.

Shushi was built to address the need for a one-stop storage location for sensitive data.  
Instead of having your credentials scattered across your projects in multiple config files, Shushi offers an encrypted vault with access via a CLI application and an API.

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

## Advanced Usage
[API Cookbook](./docs/api_cookbook.md)  
[Environment Variables](./docs/environment_variables.md)

## Contribute
Contributions are welcomed, please see the [contributions guide](./CONTRIBUTE.md).
