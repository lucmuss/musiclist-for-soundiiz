#!/bin/bash
# Example usage for MusicList for Soundiiz

# 1. Simple CSV export
echo "=== Example 1: Simple CSV export ==="
musiclist-for-soundiiz -i ~/Music -o soundiiz_playlist.csv

# 2. Only MP3 and FLAC files
echo -e "\n=== Example 2: Only MP3 and FLAC ==="
musiclist-for-soundiiz -i ~/Music -e .mp3 .flac -o high_quality.csv

# 3. JSON export with full metadata
echo -e "\n=== Example 3: JSON export ==="
musiclist-for-soundiiz -i ~/Music -o music_backup.json -f json

# 4. Create M3U playlist
echo -e "\n=== Example 4: M3U playlist ==="
musiclist-for-soundiiz -i ~/Music -o my_playlist.m3u -f m3u

# 5. Verbose mode for debugging
echo -e "\n=== Example 5: Verbose mode ==="
musiclist-for-soundiiz -i ~/Music -o output.csv -v

# 6. Non-recursive (top-level only)
echo -e "\n=== Example 6: Non-recursive ==="
musiclist-for-soundiiz -i ~/Music/Favorites --no-recursive -o favorites.csv

# 7. Large library with CSV splitting
echo -e "\n=== Example 7: Large library (max 200 songs per file) ==="
musiclist-for-soundiiz -i ~/Music -o playlist.csv --max-songs-per-file 200

# 8. Quiet mode (errors only)
echo -e "\n=== Example 8: Quiet mode ==="
musiclist-for-soundiiz -i ~/Music -o output.csv -q

echo -e "\nAll examples completed."
