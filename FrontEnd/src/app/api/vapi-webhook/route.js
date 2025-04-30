import { NextResponse } from 'next/server';
import { clientService } from '../../../services/api';

export async function POST(request) {
    try {
        const { message } = await request.json();
        

        if (message?.type === 'end-of-call-report') {
            console.log('End of Call Report received:');
            
            // Parse the summary JSON string
            const summary = JSON.parse(message.analysis.summary);
            console.log('Parsed Summary:', summary);
            
            const mood = summary.mood;
            console.log('Extracted mood value:', mood);

            if (typeof mood === 'number') {
                // Record mood
                await clientService.recordMood(1, mood);
                
                // Format triggers for batch processing
                const triggersArray = summary.triggers;
                console.log('Triggers to process:', triggersArray);
                
                // Record all triggers in one batch - remove the extra wrapping
                await clientService.recordTriggersBatch(triggersArray);
            } else {
                console.error('Invalid mood value:', mood);
            }
        }

        return NextResponse.json({ status: 'success' });
    } catch (error) {
        console.error('Webhook error:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
} 