# Shrink Windows Partition for Dual Boot

If you plan to dual-boot Arch Linux alongside Windows, you must shrink your C: drive after the Windows installation finishes:

1.  Right-click the **Start Button** and select **'Disk Management'**.
2.  Locate your main Windows partition (usually **C:**).
3.  Right-click the **C:** partition and select **'Shrink Volume...'**.
4.  In the field **'Enter the amount of space to shrink in MB'**, enter a value that leaves your desired amount for Windows.
    *   *> Formula: `Total Size (MB) - Desired Windows Size (MB) = Amount to Shrink (MB)`*
    *   *> Example: To leave exactly **250 GB** for Windows (which is roughly **256,000 MB**): `Total Size (MB) - 256000 = Enter this result`.*
5.  Click **'Shrink'**.
6.  You will see **'Unallocated'** space appear, which you can leave unformatted so Arch Linux can use it later.
