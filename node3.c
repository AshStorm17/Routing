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
} dt3;

void rtinit3() 
{
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            dt3.costs[i][j] = MAXCOST;
        }
    }

    // Set direct link costs
    dt3.costs[0][0] = 7;
    dt3.costs[2][2] = 2;
    dt3.costs[3][3] = 0;

    struct rtpkt pkt;
    pkt.sourceid = 3;

    for (int i = 0; i < 4; i++)
    {
        int min = MAXCOST;
        for (int j = 0; j < 4; j++)
        {
            if (dt3.costs[i][j] < min)
            {
                min = dt3.costs[i][j];
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


void rtupdate3(rcvdpkt) struct rtpkt *rcvdpkt;
{
    int src = rcvdpkt->sourceid;
    int updated = 0;

    // Get the direct link cost to the source
    int direct_link_cost;
    switch (src) {
        case 0: direct_link_cost = 7; break;
        case 2: direct_link_cost = 2; break;
        default: return; // Not a direct neighbor, ignore
    }

    // Update cost table entries for each destination
    for (int i = 0; i < 4; i++)
    {
        // Calculate the new cost to reach node i through the source
        int new_cost = direct_link_cost + rcvdpkt->mincost[i];

        // If the new cost is less than the current cost, update it
        if (new_cost < dt3.costs[src][i])
        {
            dt3.costs[src][i] = new_cost;
            updated = 1;
        }
    }

    if (updated)
    {
        // Send updated costs to neighbors
        struct rtpkt pkt;
        pkt.sourceid = 3;

        for (int i = 0; i < 4; i++)
        {
            int min = MAXCOST;
            for (int j = 0; j < 4; j++)
            {
                if (dt3.costs[j][i] < min)
                {
                    min = dt3.costs[j][i];
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


printdt3(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via     \n");
  printf("   D3 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 1|  %3d   %3d\n",dtptr->costs[1][0], dtptr->costs[1][2]);
  printf("     2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);

}
