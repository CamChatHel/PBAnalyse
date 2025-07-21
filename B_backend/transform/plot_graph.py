def create_measurement_graph(measurement_data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    import io
    import base64

    xticks = [63, 125, 250, 500, 1000, 2000, 4000]
    x = []
    y = []

    for k in measurement_data.keys():
        try:
            freq = int(k[1:])
            value = measurement_data[k].strip()
            if value == "/" or value == "0" or value == "0.0" or value == "-":
                x.append(freq)
                y.append(None)  # Lücke im Graph
            else:
                x.append(freq)
                y.append(float(value))
        except:
            continue  # Fehlerhafte Werte ignorieren

    plt.figure(figsize=(5.8, 7.5))
    plt.plot(x, y, marker='.', linestyle='-')

    plt.xscale('log')
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.xticks(xticks, labels=[str(t) for t in xticks])
    plt.xlim(50, 5000)
    # Oktavfrequenzen (durchgezogene Linien)
    xticks = [63, 125, 250, 500, 1000, 2000, 4000]
    for tick in xticks:
        plt.axvline(tick, color='gray', linestyle='-', linewidth=0.4)

    # Terzfrequenzen (gestrichelte Linien)
    extra_freq_values = [
        50, 63, 80, 100, 125, 160, 200, 250, 315, 400,
        500, 630, 800, 1000, 1250, 1600, 2000, 2500,
        3150, 4000, 5000
    ]

    # Nur gestrichelte Linien für Frequenzen, die nicht in xticks sind
    for tick in extra_freq_values:
        if tick not in xticks:
            plt.axvline(tick, color='gray', linestyle='--', linewidth=0.3)

    plt.title("Übertragene Messdaten", fontsize=10)
    plt.xlabel("Frequenz (Hz)")
    plt.ylabel("Messwert (dB)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
    # Dynamisch: Y-Grenzen berechnen (ignoriere None)
    valid_y = [val for val in y if val is not None]
    if valid_y:
        min_val = int(min(valid_y))
        max_val = int(max(valid_y))

        # Mittelwert berechnen und auf ganze Zahl runden
        center = round((min_val + max_val) / 2)

        # 50er Bereich definieren, symmetrisch um center
        ymin = center - 30
        ymax = center + 30

        # Y-Achsenbereich setzen
        plt.ylim(ymin, ymax)

        # Horizontale Hilfslinien zeichnen
        for ytick in range(ymin, ymax + 1):
            linestyle = '-' if ytick % 10 == 0 else ':'
            linewidth = 0.4 if ytick % 10 == 0 else 0.2
            plt.axhline(ytick, color='gray', linestyle=linestyle, linewidth=linewidth)

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{graph_url}"
