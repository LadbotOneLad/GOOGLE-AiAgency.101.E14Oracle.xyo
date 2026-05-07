while (True) {
    \ = Get-Date -Format o
    \ = Get-Content .\config\timing.json | ConvertFrom-Json

    \ = @{
        timestamp = \
        anchor_micro = \.anchor_micro
        anchor_health = \.anchor_health
        anchor_macro = \.anchor_macro
        moment_internal = \.moment_internal
    } | ConvertTo-Json -Depth 5

    Set-Content -Path ".heartbeat\pulse.json" -Value \

    Start-Sleep -Milliseconds 150
}
