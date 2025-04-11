#include <stdio.h>

#define MAXCOST 999

extern struct rtpkt
{
    int sourceid;   // id of router sending this pkt
    int destid;     // id of router to which pkt being sent
    int mincost[4]; // min cost to node 0 ... 3
};

extern int TRACE;
extern int YES;
extern int NO;

int connectcosts1[4] = {1, 0, 1, 999};

struct distance_table
{
    int costs[4][4];
} dt1;

rtinit1()
{
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            dt1.costs[i][j] = MAXCOST;
        }
    }

    // Set direct link costs
    dt1.costs[0][0] = 1;
    dt1.costs[1][1] = 0;
    dt1.costs[2][2] = 1;

    struct rtpkt pkt;
    pkt.sourceid = 1;

    for (int i = 0; i < 4; i++)
    {
        int min = MAXCOST;
        for (int j = 0; j < 4; j++)
        {
            if (dt1.costs[i][j] < min)
            {
                min = dt1.costs[i][j];
            }
        }
        pkt.mincost[i] = min;
    }

    // Send to neighbors: 0, 2
    pkt.destid = 0;
    tolayer2(pkt);

    pkt.destid = 2;
    tolayer2(pkt);
}

rtupdate1(rcvdpkt) struct rtpkt *rcvdpkt;
{
    int src = rcvdpkt->sourceid;
    int updated = 0;

    // Get the direct link cost to the source
    int direct_link_cost;
    switch (src) {
        case 0: direct_link_cost = 1; break;
        case 2: direct_link_cost = 1; break;
        default: return; // Not a direct neighbor, ignore
    }

    // Update cost table entries for each destination
    for (int i = 0; i < 4; i++)
    {
        // Calculate the new cost to reach node i through the source
        int new_cost = direct_link_cost + rcvdpkt->mincost[i];

        // If the new cost is less than the current cost, update it
        if (new_cost < dt1.costs[src][i])
        {
            dt1.costs[0][i] = new_cost;
            updated = 1;
        }
    }

    if (updated)
    {
        // Send updated costs to neighbors
        struct rtpkt pkt;
        pkt.sourceid = 1;

        for (int i = 0; i < 4; i++)
        {
            int min = MAXCOST;
            for (int j = 0; j < 4; j++)
            {
                if (dt1.costs[i][j] < min)
                {
                    min = dt1.costs[i][j];
                }
            }
            pkt.mincost[i] = min;
        }

        // Send to neighbors: 0, 2
        pkt.destid = 0;
        tolayer2(pkt);

        pkt.destid = 2;
        tolayer2(pkt);
    }
}

printdt1(dtptr) struct distance_table *dtptr;

{
    printf("             via   \n");
    printf("   D1 |    0     2 \n");
    printf("  ----|-----------\n");
    printf("     0|  %3d   %3d\n", dtptr->costs[0][0], dtptr->costs[0][2]);
    printf("dest 2|  %3d   %3d\n", dtptr->costs[2][0], dtptr->costs[2][2]);
    printf("     3|  %3d   %3d\n", dtptr->costs[3][0], dtptr->costs[3][2]);
}

linkhandler1(linkid, newcost) int linkid, newcost;
/* called when cost from 1 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */

{
}
