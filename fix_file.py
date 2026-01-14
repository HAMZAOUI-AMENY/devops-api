with open('app/main.py', 'r') as f:
    content = f.read()

# Remove all trailing whitespace and newlines
content = content.rstrip()

# Add exactly one newline at the end
content = content + '\n'

with open('app/main.py', 'w', newline='\n') as f:
    f.write(content)

print("File fixed!")