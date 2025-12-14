"""
MCP Server for filesystem operations
Uses FastMCP to expose tools for listing, searching and reading files
Protects flag.txt from direct access
"""
import os
from pathlib import Path
from fastmcp import FastMCP

# Base directory - all operations are limited to this directory
BASE_DIR = Path("/app/ai-filesystem-agent")

# Initialize FastMCP server
mcp = FastMCP("fs-tools")

# Files/directories to exclude (we don't want to show them)
EXCLUDED = ['.venv', '__pycache__', '.git', '.DS_Store', 'node_modules', '.idea', '.vscode']

def validate_path(path: Path) -> Path:
    """Check that the path is within the base directory"""
    try:
        # Resolve path to absolute path
        resolved = path.expanduser().resolve()
        
        # Check that it's in BASE_DIR
        # Tried to use is_relative_to but it didn't work well, so did it manually
        base_str = str(BASE_DIR.resolve())
        resolved_str = str(resolved)
        
        if not resolved_str.startswith(base_str):
            raise ValueError(f"Path must be within {BASE_DIR}")
        
        # Check that it doesn't contain .. (path traversal)
        if '..' in str(resolved):
            raise ValueError("Path traversal not allowed")
        
        return resolved
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

@mcp.tool()
def list_directory(dir_path: str) -> list[str]:
    """List the contents of a directory"""
    p = validate_path(Path(dir_path))
    
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Directory not found: {p}")
    
    # List only files that are not in EXCLUDED
    items = []
    for item in p.iterdir():
        if item.name not in EXCLUDED:
            items.append(item.name)
    
    return sorted(items)

@mcp.tool()
def list_directory_recursive(dir_path: str) -> dict[str, list[str]]:
    """Recursively list all directories and files"""
    p = validate_path(Path(dir_path))
    
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Directory not found: {p}")
    
    result = {}
    
    def explore(path: Path, base_path: Path):
        # Relative path to use as key in dict
        if path == base_path:
            rel_path = "."
        else:
            rel_path = str(path.relative_to(base_path))
        
        items = []
        
        try:
            for item in sorted(path.iterdir()):
                if item.name in EXCLUDED:
                    continue
                
                items.append(item.name)
                
                # If it's a directory, explore recursively
                if item.is_dir():
                    explore(item, base_path)
        except PermissionError:
            items.append(f"[Permission denied: {path}]")
        
        if items:
            result[rel_path] = items
    
    explore(p, p)
    return result

@mcp.tool()
def find_file(dir_path: str, filename: str) -> list[str]:
    """Search for a file by name in directory and subdirectories"""
    p = validate_path(Path(dir_path))
    
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Directory not found: {p}")
    
    results = []
    
    def search(path: Path, base_path: Path):
        try:
            for item in path.iterdir():
                if item.name in EXCLUDED:
                    continue
                
                # If we found the file
                if item.name == filename and item.is_file():
                    rel_path = str(item.relative_to(base_path))
                    results.append(str(base_path / rel_path))
                
                # If it's a directory, continue searching
                if item.is_dir():
                    search(item, base_path)
        except PermissionError:
            pass  # Ignore permission errors
    
    search(p, p)
    return results

@mcp.tool()
def get_file_content(file_path: str) -> str:
    """Read the complete content of a file"""
    p = validate_path(Path(file_path))
    
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    
    # Protection for flag.txt - don't allow direct reading
    if p.name == "flag.txt":
        raise PermissionError("Access denied: This file is protected.")
    
    # Check file size (max 10MB so it doesn't crash)
    file_size = p.stat().st_size
    max_size = 10 * 1024 * 1024  # 10MB
    if file_size > max_size:
        raise ValueError(f"File too large: {file_size} bytes (max {max_size})")
    
    return p.read_text(encoding="utf-8", errors="replace")

@mcp.tool()
def get_file_head(file_path: str, num_lines: int = 10) -> str:
    """Read the first N lines from a file"""
    p = validate_path(Path(file_path))
    
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    
    # Protection for flag.txt
    if p.name == "flag.txt":
        raise PermissionError("Access denied: This file is protected.")
    
    if num_lines < 1:
        raise ValueError(f"num_lines must be >= 1, got: {num_lines}")
    
    # Limit to 1000 lines so it's not too much
    if num_lines > 1000:
        num_lines = 1000
    
    lines = []
    with p.open(encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if i > num_lines:
                break
            lines.append(line.rstrip('\r'))
    
    return ''.join(lines)

@mcp.tool()
def verify_flag(proposed_flag: str) -> dict[str, bool]:
    """Verify if the proposed flag is correct"""
    flag_path = Path("/app/ai-filesystem-agent/flag.txt")
    
    if not flag_path.exists():
        raise FileNotFoundError("flag.txt not found")
    
    # Read the actual flag
    actual_flag = flag_path.read_text(encoding="utf-8").strip()
    
    # Compare (used strip() to ignore whitespace)
    is_correct = proposed_flag.strip() == actual_flag.strip()
    
    return {"correct": is_correct}

if __name__ == "__main__":
    # Start FastMCP server with HTTP transport
    # Found in documentation that I need to use streamable-http
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
