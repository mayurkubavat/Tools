source /tools/Xilinx/2025.1/Vivado/settings64.sh

# Add DV/git/Tools to PATH if not already present
case ":$PATH:" in
  *":$DV/git/Tools:"*) ;; # Already in PATH, do nothing
  *) export PATH="$PATH:$DV/git/Tools" ;; # Not in PATH, add it
esac
