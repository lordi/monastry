(

// global pitch Offset, can be used to transpose the whole song
~pitchOffset = 60;

// global duration divisor, can be used to make the song faster or slower
~durParam = 6.5;

// *************************** SynthDefs ***************************

// SynthDef for the first and second voice
SynthDef("mario", { |out, amp=0.3, freq=440|
	var snd;
	snd = LFPulse.ar(freq)!2;
	snd = snd * EnvGen.ar(Env.linen(0.001, 0.1, 0.03), doneAction:2);
	OffsetOut.ar(out, snd*amp);
}).send(s);

// SynthDef for the bass
y = SynthDef("bass", { |out, amp=0.5, freq=440|
	var snd;
	snd = LFTri.ar(freq)!2;
	snd = snd * EnvGen.ar(Env.linen(0.001, 0.1, 0.03), doneAction:2);
	OffsetOut.ar(out, snd*amp);
}).send(s);

// SynthDef for percussion sounds
z = SynthDef("beat", { |out, amp=0.3, sustain=0.01|
	var snd;
	snd = WhiteNoise.ar()!2;
	snd = HPF.ar(snd, 2000);
	snd = snd * EnvGen.ar(Env.linen(0.005, sustain, 0.01), doneAction:2);
	OffsetOut.ar(out, snd*amp);
}).send(s);

0.exit;
)
