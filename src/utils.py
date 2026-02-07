import nflreadpy

_TEAM_COLORS_CACHE = None

def get_team_colors_map():
    """
    Fetches official team colors using nflreadpy and returns a mapping.
    Caches the result to avoid repeated API calls.
    """
    global _TEAM_COLORS_CACHE
    if _TEAM_COLORS_CACHE is not None:
        return _TEAM_COLORS_CACHE

    try:
        teams_df = nflreadpy.load_teams()
        mapping = {}
        for row in teams_df.to_dicts():
            mapping[row["team_abbr"]] = {
                "primary": row["team_color"] if row["team_color"] else "#000000",
                "secondary": row["team_color2"] if row["team_color2"] else "#FFFFFF",
            }
        _TEAM_COLORS_CACHE = mapping
        return mapping
    except Exception as e:
        print(f"Warning: Could not load team colors: {e}")
        return {}

def hex_to_rgb(hex_color):
    """
    Converts a hex color string (e.g., '#E31837') to an RGB tuple (0-255).
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    """
    Calculates the Euclidean distance between two RGB colors.
    """
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

def get_distinct_colors(home_colors, visitor_colors, threshold=50):
    """
    Ensures that the primary colors for home and visitor are distinct enough.
    If they are too similar (distance < threshold), switches visitor to their secondary color.
    """
    h_primary = hex_to_rgb(home_colors["primary"])
    v_primary = hex_to_rgb(visitor_colors["primary"])
    
    if color_distance(h_primary, v_primary) < threshold:
        # Switch visitor to secondary color
        return home_colors["primary"], visitor_colors["secondary"]
    
    return home_colors["primary"], visitor_colors["primary"]
