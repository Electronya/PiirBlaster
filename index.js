// Load dependencies
const Gpio = require('onoff');

console.log('Starting Module\n');

// Emitter GPIO
const out0 = new Gpio(4, 'in', 'both');
// const out1 = new Gpio(17, { mode: Gpio.OUTPUT });
// const out2 = new Gpio(27, { mode: Gpio.OUTPUT });
// const out3 = new Gpio(22, { mode: Gpio.OUTPUT });
// const out4 = new Gpio(10, { mode: Gpio.OUTPUT });
// const out5 = new Gpio(9, { mode: Gpio.OUTPUT });

// Receiver GPIO
// const in0 = new Gpio(11, { mode: Gpio.INPUT, alert: true, edge: Gpio.EITHER_EDGE });

// // Tick variable
// let fallingEdgeTick = 0;
// let raisingEdgeTick = 0;

// const readingInput = () => {
//   // Reading Receiver
//   in0.on('alert', (level, tick) => {
//     if (level === 0) {
//       console.log('Falling edge detected\n');
//       fallingEdgeTick = tick;
//       if (raisingEdgeTick !== 0) {
//         const highPulseWidth = (fallingEdgeTick - raisingEdgeTick);
//         console.log(`High pulse width: ${highPulseWidth} us\n`);
//         // out0.trigger(highPulseWidth, 1);
//         // out1.trigger(highPulseWidth, 1);
//         // out2.trigger(highPulseWidth, 1);
//         // out3.trigger(highPulseWidth, 1);
//         // out4.trigger(highPulseWidth, 1);
//         // out5.trigger(highPulseWidth, 1);
//       }
//     } else {
//       console.log('Raising edge detected\n');
//       raisingEdgeTick = tick;
//       const lowPulseWidth = (raisingEdgeTick - fallingEdgeTick);
//       console.log(`Low pPulse width: ${lowPulseWidth} us\n`);
//     }
//   });
// };

// readingInput();
