#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import sdl2
import sdl2.ext

commands = {}

def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_TIMER | sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_HAPTIC)
    numOfDevices = sdl2.SDL_NumHaptics()
    status  = 0
    if(numOfDevices is 0):
        print('No Force Feedback devices found')
        print('Stopping...')
    elif(numOfDevices is 1):
        print('Found one device')
        status = test(0)
    else:
        print('Found %s Number of devices:' % numOfDevices)
        for index in range(0, numOfDevices):
            print('{index}: {deviceName}'.format(index=index, deviceName=sdl2.SDL_HapticName(index).decode("utf-8")))
    
    sdl2.SDL_Quit()
    return status


def test(index):
    print('Selected device {index}: {deviceName} \n'.format(index=index, deviceName=sdl2.SDL_HapticName(index).decode("utf-8")))

    #Try to open device
    device = sdl2.SDL_HapticOpen(index)
    if(device is None):
        print('Error opening device!')
        return -1

    #Print supported effects
    print('Effect support:')
    print('\t[]Custom:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_CUSTOM)))
    print('\t[0]Constant:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_CONSTANT)))
    print('\t[1]Sine:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_SINE)))
    print('\t[2]LeftRight:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_LEFTRIGHT)))
    print('\t[3]Triangle:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_TRIANGLE)))
    print('\t[4]SawtoothUp:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_SAWTOOTHUP)))
    print('\t[5]SawtoothDown:\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_SAWTOOTHDOWN)))
    print('\t[6]Ramp:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_RAMP)))
    print('\t[7]Spring:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_SPRING)))
    print('\t[8]Damper:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_DAMPER)))
    print('\t[9]Inertia:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_INERTIA)))
    print('\t[A]Friction:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_FRICTION)))

    print('\nEffect features:')
    print('\t[B]Gain:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_GAIN)))
    print('\t[C]Autocenter:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_AUTOCENTER)))
    print('\t[D]Pauze:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_PAUSE)))
    print('\t[E]Status:\t\t{!s}'.format(checkSupported(device, sdl2.SDL_HAPTIC_STATUS)))

    while(True):
        print('\nSelect an option (or q to quit): ')
        selection = input()
        if(selection is 'q'):
            break
        command = commands.get(selection.upper())
        if(command is None):
            print('Unknown command')
        else:
            command(device)

    sdl2.SDL_HapticClose(device)

def checkSupported(device, feature):
    return (feature & sdl2.SDL_HapticQuery(device) is not 0)

def test_constant(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_CONSTANT)):
        print('Constant Force not supported')
        return
    print('Testing Constant...')

    length = int(input("length: "))
    attack_length = int(input("attack_length: "))
    fade_length = int(input("fade_length: "))
    level = int(input("level: "))
    direction = int(input("direction: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_CONSTANT, constant= \
            sdl2.SDL_HapticConstant(type=sdl2.SDL_HAPTIC_CONSTANT, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(direction,0,0)), \
            length=length, level=level, attack_length=attack_length, fade_length=fade_length))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(5000)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_sine(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_SINE)):
        print('Sine Force not supported')
        return
    print('Testing Sine...')

    period = int(input("period: "))
    magnitude = int(input("magnitude: "))
    length = int(input("length: "))
    attack_length = int(input("attack_length: "))
    fade_length = int(input("fade_length: "))
    direction = int(input("direction: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SINE, periodic= \
            sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SINE, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(direction,0,0)), \
            period=period, magnitude=magnitude, length=length, attack_length=attack_length, fade_length=fade_length))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_left_right(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_LEFTRIGHT)):
        print('LeftRight Force not supported')
        return
    print('Testing LeftRight...')

    l_magnitude = int(input("large magnitude: "))
    s_magnitude = int(input("small magnitude: "))
    length = int(input("length: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_LEFTRIGHT, leftright= \
            sdl2.SDL_HapticLeftRight(type=sdl2.SDL_HAPTIC_LEFTRIGHT, length=length, large_magnitude=l_magnitude, small_magnitude=s_magnitude))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_triangle(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_TRIANGLE)):
        print('Trianglewave Force not supported')
        return
    print('Testing Trianglewave...')

    period = int(input("period: "))
    magnitude = int(input("magnitude: "))
    length = int(input("length: "))
    attack_length = int(input("attack_length: "))
    fade_length = int(input("fade_length: "))
    direction = int(input("direction: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_TRIANGLE, periodic= \
            sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SINE, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(direction,0,0)), \
            period=period, magnitude=magnitude, length=length, attack_length=attack_length, fade_length=fade_length))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_SawtoothUp(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_SAWTOOTHUP)):
        print('SawtoothUp Force not supported')
        return
    print('Testing SawtoothUp...')

    period = int(input("period: "))
    magnitude = int(input("magnitude: "))
    length = int(input("length: "))
    attack_length = int(input("attack_length: "))
    fade_length = int(input("fade_length: "))
    direction = int(input("direction: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SAWTOOTHUP, periodic= \
            sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SAWTOOTHUP, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(direction,0,0)), \
            period=period, magnitude=magnitude, length=length, attack_length=attack_length, fade_length=fade_length))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_SawtoothDown(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_SAWTOOTHDOWN)):
        print('SawtoothDown Force not supported')
        return
    print('Testing SawtoothDown...')

    period = int(input("period: "))
    magnitude = int(input("magnitude: "))
    length = int(input("length: "))
    attack_length = int(input("attack_length: "))
    fade_length = int(input("fade_length: "))
    direction = int(input("direction: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SAWTOOTHDOWN, periodic= \
            sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SAWTOOTHDOWN, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(direction,0,0)), \
            period=period, magnitude=magnitude, length=length, attack_length=attack_length, fade_length=fade_length))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_ramp(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_RAMP)):
        print('Ramp Force not supported')
        return
    print('Testing Ramp...')

    start = int(input("start force: "))
    end = int(input("end force: "))
    length = int(input("length: "))
    attack_length = int(input("attack_length: "))
    fade_length = int(input("fade_length: "))
    direction = int(input("direction: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_RAMP, ramp= \
            sdl2.SDL_HapticRamp(type=sdl2.SDL_HAPTIC_RAMP, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(direction,0,0)), \
            start=start, end=end, length=length, attack_length=attack_length, fade_length=fade_length))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_spring(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_SPRING)):
        print('Spring Force not supported')
        return
    print('Testing Spring...')

    right_sat = int(input("right_sat: "))
    left_sat = int(input("left_sat: "))
    right_coeff = int(input("right_coeff: "))
    left_coeff = int(input("left_coeff: "))
    center = int(input("center: "))
    length = int(input("length: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SPRING, condition= \
            sdl2.SDL_HapticCondition(type=sdl2.SDL_HAPTIC_SPRING, length=length, right_sat=(right_sat,right_sat,right_sat), left_sat=(left_sat,left_sat,left_sat), \
            right_coeff=(right_coeff,right_coeff,right_coeff), left_coeff=(left_coeff,left_coeff,left_coeff), center=(center,center,center)))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_damper(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_DAMPER)):
        print('Damper Force not supported')
        return
    print('Testing damper...')

    right_sat = int(input("right sat: "))
    left_sat = int(input("left sat: "))
    right_coeff = int(input("right coeff: "))
    left_coeff = int(input("left coeff: "))
    center = int(input("center: "))
    length = int(input("length: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_DAMPER, condition= \
            sdl2.SDL_HapticCondition(type=sdl2.SDL_HAPTIC_DAMPER, length=length, right_sat=(right_sat,right_sat,right_sat), left_sat=(left_sat,left_sat,left_sat), \
            right_coeff=(right_coeff,right_coeff,right_coeff), left_coeff=(left_coeff,left_coeff,left_coeff), center=(center,center,center)))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_inertia(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_INERTIA)):
        print('Inertia Force not supported')
        return
    print('Testing inertia...')

    right_sat = int(input("right sat: "))
    left_sat = int(input("left sat: "))
    right_coeff = int(input("right coeff: "))
    left_coeff = int(input("left coeff: "))
    center = int(input("center: "))
    length = int(input("length: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_INERTIA, condition= \
            sdl2.SDL_HapticCondition(type=sdl2.SDL_HAPTIC_INERTIA, length=length, right_sat=(right_sat,right_sat,right_sat), left_sat=(left_sat,left_sat,left_sat), \
            right_coeff=(right_coeff,right_coeff,right_coeff), left_coeff=(left_coeff,left_coeff,left_coeff), center=(center,center,center)))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_friction(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_FRICTION)):
        print('Friction Force not supported')
        return
    print('Testing friction...')

    right_sat = int(input("right sat: "))
    left_sat = int(input("left sat: "))
    right_coeff = int(input("right coeff: "))
    left_coeff = int(input("left coeff: "))
    center = int(input("center: "))
    length = int(input("length: "))

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_FRICTION, condition= \
            sdl2.SDL_HapticCondition(type=sdl2.SDL_HAPTIC_FRICTION, length=length, right_sat=(right_sat,right_sat,right_sat), left_sat=(left_sat,left_sat,left_sat), \
            right_coeff=(right_coeff,right_coeff,right_coeff), left_coeff=(left_coeff,left_coeff,left_coeff), center=(center,center,center)))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(length)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def set_gain(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_GAIN)):
        print('Setting gain not supported')
        return
    print('Setting gain...')

    gain = int(input("gain (0-100): "))
    sdl2.SDL_HapticSetGain(device, gain)

def set_autocenter(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_AUTOCENTER)):
        print('Setting autocenter not supported')
        return
    print('Setting autocenter...')

    autocenter = bool(input("autocenter (0 - 1): "))
    sdl2.SDL_HapticSetAutocenter(device, autocenter)

def test_pauze(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_PAUSE)):
        print('Pauzing not supported')
        return
    print('Testing pauzing...')

    if(not checkSupported(device, sdl2.SDL_HAPTIC_SINE)):
        print('Sine Force not supported')
        return
    print('Testing Sine...')

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SINE, periodic= \
            sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SINE, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(9000,0,0)), \
            period=4000, magnitude=4000, length=5000, attack_length=1000, fade_length=1000))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    sdl2.SDL_Delay(2500)
    sdl2.SDL_HapticPause(device)
    sdl2.SDL_Delay(2500)
    sdl2.SDL_HapticUnpause(device)
    sdl2.SDL_Delay(2500)
    sdl2.SDL_HapticDestroyEffect(device, effect_id)

def test_status(device):
    if(not checkSupported(device, sdl2.SDL_HAPTIC_STATUS)):
        print('Getting status not supported')
        return
    print('Getting status...')

    if(not checkSupported(device, sdl2.SDL_HAPTIC_SINE)):
        print('Sine Force not supported')
        return
    print('Testing Sine...')

    effect = sdl2.SDL_HapticEffect(type=sdl2.SDL_HAPTIC_SINE, periodic= \
            sdl2.SDL_HapticPeriodic(type=sdl2.SDL_HAPTIC_SINE, direction=sdl2.SDL_HapticDirection(type=sdl2.SDL_HAPTIC_POLAR, dir=(9000,0,0)), \
            period=4000, magnitude=4000, length=5000, attack_length=1000, fade_length=1000))


    effect_id = sdl2.SDL_HapticNewEffect(device, effect)
    print('status: {}'.format(sdl2.SDL_HapticGetEffectStatus(device, effect_id)))
    sdl2.SDL_HapticRunEffect(device, effect_id, 1)
    print('status: {}'.format(sdl2.SDL_HapticGetEffectStatus(device, effect_id)))
    sdl2.SDL_Delay(2500)
    print('status: {}'.format(sdl2.SDL_HapticGetEffectStatus(device, effect_id)))
    sdl2.SDL_Delay(2500)
    print('status: {}'.format(sdl2.SDL_HapticGetEffectStatus(device, effect_id)))
    sdl2.SDL_Delay(2500)
    print('status: {}'.format(sdl2.SDL_HapticGetEffectStatus(device, effect_id)))
    sdl2.SDL_HapticDestroyEffect(device, effect_id)
    print('status: {}'.format(sdl2.SDL_HapticGetEffectStatus(device, effect_id)))


    

if __name__ == "__main__":
    commands = {'0': test_constant, '1': test_sine, '2': test_left_right, 
            '3': test_triangle, '4': test_SawtoothUp, '5': test_SawtoothDown, 
            '6': test_ramp, '7': test_spring, '8': test_damper, 
            '9': test_inertia, 'A': test_friction, 'B': set_gain, 
            'C': set_autocenter, 'D': test_pauze, 'E': test_status}
    sys.exit(main())