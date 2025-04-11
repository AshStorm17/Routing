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

struct distance_table
{
    int costs[4][4];
} dt0;

void rtinit0()
{
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            dt0.costs[i][j] = MAXCOST;
        }
    }

    // Set direct link costs
    dt0.costs[0][0] = 0;
    dt0.costs[1][1] = 1;
    dt0.costs[2][2] = 3;
    dt0.costs[3][3] = 7;

    struct rtpkt pkt;
    pkt.sourceid = 0;

    for (int i = 0; i < 4; i++)
    {
        int min = MAXCOST;
        for (int j = 0; j < 4; j++)
        {
            if (dt0.costs[i][j] < min)
            {
                min = dt0.costs[i][j];
            }
        }
        pkt.mincost[i] = min;
    }

    // Send to neighbors: 1, 2, 3
    pkt.destid = 1;
    tolayer2(pkt);

    pkt.destid = 2;
    tolayer2(pkt);

    pkt.destid = 3;
    tolayer2(pkt);
}

void rtupdate0(rcvdpkt) struct rtpkt *rcvdpkt;
{
    int src = rcvdpkt->sourceid;
    int updated = 0;

    // Get the direct link cost to the source
    int direct_link_cost;
    switch (src) {
        case 1: direct_link_cost = 1; break;
        case 2: direct_link_cost = 3; break;
        case 3: direct_link_cost = 7; break;
        default: return; // Not a direct neighbor, ignore
    }

    // Update cost table entries for each destination
    for (int i = 0; i < 4; i++)
    {
        // Calculate the new cost to reach node i through the source
        int new_cost = direct_link_cost + rcvdpkt->mincost[i];

        // If the new cost is less than the current cost, update it
        if (new_cost < dt0.costs[src][i])
        {
            dt0.costs[src][i] = new_cost;
            updated = 1;
        }
    }

    if (updated)
    {
        // Send updated costs to neighbors
        struct rtpkt pkt;
        pkt.sourceid = 0;

        for (int i = 0; i < 4; i++)
        {
            int min = MAXCOST;
            for (int j = 0; j < 4; j++)
            {
                if (dt0.costs[j][i] < min)
                {
                    min = dt0.costs[j][i];
                }
            }
            pkt.mincost[i] = min;
        }

        // Send to neighbors: 1, 2, 3
        pkt.destid = 1;
        tolayer2(pkt);

        pkt.destid = 2;
        tolayer2(pkt);

        pkt.destid = 3;
        tolayer2(pkt);
    }
}

printdt0(dtptr) struct distance_table *dtptr;

{
    printf("                via     \n");
    printf("   D0 |    1     2    3 \n");
    printf("  ----|-----------------\n");
    printf("     1|  %3d   %3d   %3d\n", dtptr->costs[1][1],
           dtptr->costs[1][2], dtptr->costs[1][3]);
    printf("dest 2|  %3d   %3d   %3d\n", dtptr->costs[2][1],
           dtptr->costs[2][2], dtptr->costs[2][3]);
    printf("     3|  %3d   %3d   %3d\n", dtptr->costs[3][1],
           dtptr->costs[3][2], dtptr->costs[3][3]);
}

linkhandler0(linkid, newcost) int linkid, newcost;

/* called when cost from 0 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */

{
    int oldcost = dt0.costs[linkid][linkid];
    if (oldcost == newcost) return; // No change

    // Update the cost to the neighbor itself
    dt0.costs[linkid][linkid] = newcost;

    // Recalculate costs to all destinations via this neighbor
    int updated = 0;
    for (int i = 0; i < 4; i++) {
        int new_path_cost = newcost + dt0.costs[linkid][i];
        if (new_path_cost < dt0.costs[0][i]) {
            dt0.costs[0][i] = new_path_cost;
            updated = 1;
        }

        // If this link was previously the best, and cost increased,
        // we may now need to recompute the minimum cost for that node
        if (oldcost + dt0.costs[linkid][i] == dt0.costs[0][i] && new_path_cost > dt0.costs[0][i]) {
            // Recompute min cost for destination i
            int min = MAXCOST;
            for (int j = 0; j < 4; j++) {
                if (dt0.costs[j][i] < min) {
                    min = dt0.costs[j][i];
                }
            }
            dt0.costs[0][i] = min;
            updated = 1;
        }
    }

    if (updated) {
        // Send updated costs to neighbors
        struct rtpkt pkt;
        pkt.sourceid = 0;

        for (int i = 0; i < 4; i++) {
            int min = MAXCOST;
            for (int j = 0; j < 4; j++) {
                if (dt0.costs[j][i] < min) {
                    min = dt0.costs[j][i];
                }
            }
            pkt.mincost[i] = min;
        }

        // Send to neighbors: 1, 2, 3
        pkt.destid = 1;
        tolayer2(pkt);

        pkt.destid = 2;
        tolayer2(pkt);

        pkt.destid = 3;
        tolayer2(pkt);
    }
}