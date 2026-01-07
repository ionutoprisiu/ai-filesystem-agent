"""
MCP Server for filesystem operations.
Exposes tools for listing, searching, and reading files via FastMCP.
"""
import os
from pathlib import Path
from fastmcp import FastMCP

# Restrict operations to this directory
BASE_DIR = Path("/app/ai-filesystem-agent")

mcp = FastMCP("fs-tools")

EXCLUDED = ['.venv', '__pycache__', '.git', '.DS_Store', 'node_modules', '.idea', '.vscode']

def validate_path(path: Path) -> Path:
    """Ensures path is safe and within limits"""
    try:
        resolved = path.expanduser().resolve()
        
        # Simple check: must start with BASE_DIR
        if not str(resolved).startswith(str(BASE_DIR.resolve())):
            raise ValueError(f"Access denied: {resolved} is outside {BASE_DIR}")
        
        return resolved
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")

@mcp.tool()
def list_directory(dir_path: str) -> list[str]:
    """Lists files in a directory"""
    p = validate_path(Path(dir_path))
    
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Not a directory: {p}")
    
    return sorted([item.name for item in p.iterdir() if item.name not in EXCLUDED])

@mcp.tool()
def list_directory_recursive(dir_path: str) -> dict[str, list[str]]:
    """Recursively lists all files"""
    p = validate_path(Path(dir_path))
    
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Not a directory: {p}")
    
    result = {}
    
    def explore(current_path):
        rel_path = "." if current_path == p else str(current_path.relative_to(p))
        items = []
        
        try:
            for item in sorted(current_path.iterdir()):
                if item.name in EXCLUDED:
                    continue
                
                items.append(item.name)
                if item.is_dir():
                    explore(item)
        except PermissionError:
            items.append("[Access Denied]")
            
        if items:
            result[rel_path] = items

    explore(p)
    return result

@mcp.tool()
def find_file(dir_path: str, filename: str) -> list[str]:
    """Search for a file recursively"""
    p = validate_path(Path(dir_path))
    results = []
    
    def search(current_path):
        try:
            for item in current_path.iterdir():
                if item.name in EXCLUDED:
                    continue
                
                if item.name == filename and item.is_file():
                    rel_path = str(item.relative_to(p))
                    results.append(str(p / rel_path))
                
                if item.is_dir():
                    search(item)
        except PermissionError:
            pass
            
    search(p)
    return results

@mcp.tool()
def get_file_content(file_path: str) -> str:
    """Reads a file"""
    p = validate_path(Path(file_path))
    
    if p.name == "flag.txt":
        raise PermissionError("Nice try! This file is protected.")
    
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
        
    if p.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("File is too big (>10MB)")
        
    return p.read_text(encoding="utf-8", errors="replace")

@mcp.tool()
def get_file_head(file_path: str, num_lines: int = 10) -> str:
    """Reads first N lines of a file"""
    p = validate_path(Path(file_path))
    
    if p.name == "flag.txt":
         raise PermissionError("Nice try! This file is protected.")
            
    lines = []
    with p.open(encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if i >= min(num_lines, 1000):
                break
            lines.append(line.rstrip())
            
    return '\n'.join(lines)

@mcp.tool()
def verify_flag(proposed_flag: str) -> dict[str, bool]:
    """Check if the captured flag is correct"""
    flag_path = Path("/app/ai-filesystem-agent/flag.txt")
    
    if not flag_path.exists():
        return {"error": "Flag file missing!"}
        
    actual = flag_path.read_text().strip()
    return {"correct": proposed_flag.strip() == actual}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
