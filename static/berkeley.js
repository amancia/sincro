let lastStep = -1;
const clocks = [];
const ui_clocks = document.getElementById('clocks');

const plt_iters = [];
// const plt_times = [];
const plt_clcks = document.getElementById('plot');

const layout = {
    title: { text: 'Média dos clocks' },
    autosize: false,
    width: 1600,
    height: 960,
}


function calcHours(time) {
    return `${Math.floor(time / 60 / 60)}:${Math.floor(time / 60 % 60).toString().padStart(2, '0')}:${(Math.floor(time % 60 % 60)).toString().padStart(2, '0')}`
}

async function load() {
    const { step, clocks: currentClocks } = await (await fetch("/state")).json();

    if (step !== lastStep) {
        lastStep = step;

        clocks.push(currentClocks);

        ui_clocks.innerHTML = clocks.at(-1).map(clock => `
                <div id="clock_${clock.idx + 1}" class="clock">
                    <div>Clock ${(clock.idx + 1).toString().padStart(2, '0')}</div>
                    <div>${calcHours(clock.time)}</div>
                    
                    <div>
                        <button id="clockSkew${clock.idx + 1}">Clock Skew</button>    
                        <button id="driftRate${clock.idx + 1}">Drift Rate</button>
                    </div>
        
                    <div style="display: flex; justify-content: space-between; gap: 16px;">
                        <div>D: ${clock.diffs.toFixed(2)}</div>
                        <div>V: ${clock.speed.toFixed(2)}</div>
                    </div>
                </div>
            `).join('');

        clocks.at(-1).forEach(clock => {
            document.getElementById(`clockSkew${clock.idx + 1}`).addEventListener('click', async () => await fetch(`/skew/${clock.idx}`));
            document.getElementById(`driftRate${clock.idx + 1}`).addEventListener('click', async () => await fetch(`/drift/${clock.idx}`));
        });

        if (clocks.length > 0) {
            plt_iters.push(plt_iters.length);
            // plt_times.push(clocks.at(-1).map(clock => clock.time).reduce((partialSum, a) => partialSum + a, 0) / clocks.at(-1).length);

            const num_clocks = clocks.at(0).length;
            const base = Math.min(...clocks.at(0).map(c => c.time));
            console.log(base)
            const ys = [...Array(num_clocks).keys()].map((_, i) => clocks.map(clock => clock.at(i).time - base));
            const plots = [...Array(num_clocks).keys()].map((_, i) => ({
                x: plt_iters, y: ys.at(i), mode: 'lines+markers',
                name: `Clock ${(i + 1).toString().padStart(2, '0')}`,
            }))

            // console.log(num_clocks, ys, plots);

            Plotly.newPlot(plt_clcks, plots, layout)
        }
    }
}

setInterval(load, 1025);
