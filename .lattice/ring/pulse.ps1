while ($true) {
    $edges = (Get-Content '.lattice\ring\edges.json' | ConvertFrom-Json).edges
    $now = Get-Date -Format o

    foreach ($edge in $edges) {
        $moment = @{
            from      = $edge.from
            to        = $edge.to
            timestamp = $now
        } | ConvertTo-Json -Depth 5

        Set-Content -Path ".lattice\ring\current.json" -Value $moment

        Start-Sleep -Milliseconds 150
    }
}
