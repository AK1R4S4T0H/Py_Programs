#!/bin/bash
# AK1R4S4T0H
# Set the path to the log file
log_file="/var/log/update_packages.log"

# Set the disk space threshold in bytes
disk_space_threshold=10737418240  # 10 GB

# Function to handle errors and exit
handle_error() {
  local exit_code=$1
  local error_message=$2

  echo "$(date '+%Y-%m-%d %H:%M:%S') - $error_message" >> "$log_file"
  # Add additional error handling code here if needed

  exit $exit_code
}

# Check if the current time is midnight
if [[ $(date +%H:%M) == "00:00" ]]; then
  # Check if the network is available
  if ping -q -c 1 google.com &>/dev/null; then
    # Check available disk space
    available_disk_space=$(df -B 1 --output=avail / | tail -n 1)
    if [[ $available_disk_space -lt $disk_space_threshold ]]; then
      handle_error 1 "Insufficient disk space."
    fi

    # Log the update process start
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Updating packages..." >> "$log_file"

    # Prompt for sudo password
    if sudo -v >/dev/null 2>&1; then
      # Perform the package update
      if sudo pacman -Syyu --noconfirm &>> "$log_file"; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Packages updated successfully." >> "$log_file"
        # Add success notification code here if needed
      else
        handle_error 1 "Failed to update packages."
      fi
    else
      handle_error 1 "Failed to authenticate as root. Please run the script with sudo."
    fi

    # Create GRUB snapshot
    snapshot_name="Update_$(date +%Y%m%d%H%M%S)"
    if sudo grub-btrfs snapshot -v -d /boot/grub -n "$snapshot_name" &>> "$log_file"; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') - GRUB snapshot created: $snapshot_name" >> "$log_file"
      # Add success notification code here if needed
    else
      handle_error 1 "Failed to create GRUB snapshot."
    fi

    # Perform log rotation
    if sudo logrotate -f /etc/logrotate.conf &>> "$log_file"; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') - Log rotation completed." >> "$log_file"
      # Add success notification code here if needed
    else
      handle_error 1 "Failed to perform log rotation."
    fi

  else
    handle_error 1 "Network is not available."
  fi
fi
