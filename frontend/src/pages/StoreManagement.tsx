import { useState } from 'react';
import { Store, MapPin, Phone, Mail, Plus, Edit, Trash2, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { Button } from '@components/ui/Button';

const StoreManagement = () => {
  const [stores] = useState([
    {
      id: '1',
      name: '海底捞火锅 - 三里屯店',
      address: '北京市朝阳区三里屯路19号',
      city: '北京',
      phone: '+86 10 6417 6688',
      email: 'sanlitun@haidilao.com',
      status: 'verified',
      visibility: 85,
    },
    {
      id: '2',
      name: '海底捞火锅 - 王府井店',
      address: '北京市东城区王府井大街138号',
      city: '北京',
      phone: '+86 10 6525 8899',
      email: 'wangfujing@haidilao.com',
      status: 'verified',
      visibility: 78,
    },
    {
      id: '3',
      name: '海底捞火锅 - 西单店',
      address: '北京市西城区西单北大街120号',
      city: '北京',
      phone: '+86 10 6601 2233',
      email: 'xidan@haidilao.com',
      status: 'pending',
      visibility: 62,
    },
  ]);

  const napConsistency = {
    overall: 92,
    name: 98,
    address: 88,
    phone: 95,
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="Store & NAP Management"
        subtitle="Manage locations and business information consistency"
        icon={<Store className="w-6 h-6 text-accent-400" />}
      />

      {/* NAP Consistency Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <GlassCard className="p-6">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-neutral-400">Overall NAP</p>
            <CheckCircle2 className="w-5 h-5 text-success-400" />
          </div>
          <p className="text-3xl font-bold text-neutral-50">{napConsistency.overall}%</p>
          <div className="w-full h-2 bg-neutral-800 rounded-full mt-3 overflow-hidden">
            <div
              className="h-full bg-success-500 rounded-full"
              style={{ width: `${napConsistency.overall}%` }}
            />
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <p className="text-sm text-neutral-400 mb-2">Name</p>
          <p className="text-3xl font-bold text-neutral-50">{napConsistency.name}%</p>
          <div className="w-full h-2 bg-neutral-800 rounded-full mt-3 overflow-hidden">
            <div
              className="h-full bg-primary-500 rounded-full"
              style={{ width: `${napConsistency.name}%` }}
            />
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <p className="text-sm text-neutral-400 mb-2">Address</p>
          <p className="text-3xl font-bold text-neutral-50">{napConsistency.address}%</p>
          <div className="w-full h-2 bg-neutral-800 rounded-full mt-3 overflow-hidden">
            <div
              className="h-full bg-warning-500 rounded-full"
              style={{ width: `${napConsistency.address}%` }}
            />
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <p className="text-sm text-neutral-400 mb-2">Phone</p>
          <p className="text-3xl font-bold text-neutral-50">{napConsistency.phone}%</p>
          <div className="w-full h-2 bg-neutral-800 rounded-full mt-3 overflow-hidden">
            <div
              className="h-full bg-accent-500 rounded-full"
              style={{ width: `${napConsistency.phone}%` }}
            />
          </div>
        </GlassCard>
      </div>

      {/* Action Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button icon={<Plus className="w-5 h-5" />}>
            Add Location
          </Button>
          <Button variant="secondary">
            Bulk Import
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-neutral-400">
            {stores.length} locations
          </span>
        </div>
      </div>

      {/* Store List */}
      <div className="space-y-4">
        {stores.map((store, index) => (
          <motion.div
            key={store.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <GlassCard className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <h3 className="text-lg font-semibold text-neutral-50">
                      {store.name}
                    </h3>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        store.status === 'verified'
                          ? 'bg-success-500/20 text-success-400'
                          : 'bg-warning-500/20 text-warning-400'
                      }`}
                    >
                      {store.status === 'verified' ? 'Verified' : 'Pending'}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="flex items-start gap-2">
                      <MapPin className="w-4 h-4 text-neutral-500 mt-1" />
                      <div>
                        <p className="text-sm text-neutral-400">Address</p>
                        <p className="text-neutral-200">{store.address}</p>
                      </div>
                    </div>

                    <div className="flex items-start gap-2">
                      <Phone className="w-4 h-4 text-neutral-500 mt-1" />
                      <div>
                        <p className="text-sm text-neutral-400">Phone</p>
                        <p className="text-neutral-200">{store.phone}</p>
                      </div>
                    </div>

                    <div className="flex items-start gap-2">
                      <Mail className="w-4 h-4 text-neutral-500 mt-1" />
                      <div>
                        <p className="text-sm text-neutral-400">Email</p>
                        <p className="text-neutral-200">{store.email}</p>
                      </div>
                    </div>

                    <div className="flex items-start gap-2">
                      <Store className="w-4 h-4 text-neutral-500 mt-1" />
                      <div>
                        <p className="text-sm text-neutral-400">LLM Visibility</p>
                        <div className="flex items-center gap-2">
                          <p className="text-neutral-200 font-semibold">{store.visibility}%</p>
                          <div className="w-20 h-2 bg-neutral-800 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${
                                store.visibility >= 80
                                  ? 'bg-success-500'
                                  : store.visibility >= 60
                                  ? 'bg-warning-500'
                                  : 'bg-error-500'
                              }`}
                              style={{ width: `${store.visibility}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 ml-4">
                  <Button variant="ghost" size="sm" icon={<Edit className="w-4 h-4" />}>
                    Edit
                  </Button>
                  <Button variant="ghost" size="sm" icon={<Trash2 className="w-4 h-4" />}>
                    Delete
                  </Button>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {/* NAP Audit */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          NAP Consistency Audit
        </h2>
        <div className="space-y-4">
          <div className="p-4 bg-success-500/10 border border-success-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-success-400 mt-1" />
              <div>
                <h3 className="text-success-400 font-semibold mb-1">
                  Name Consistency: Excellent
                </h3>
                <p className="text-sm text-neutral-400">
                  98% consistency across all LLM engines. Minor variations detected in 2 instances.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-warning-500/10 border border-warning-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <MapPin className="w-5 h-5 text-warning-400 mt-1" />
              <div>
                <h3 className="text-warning-400 font-semibold mb-1">
                  Address Consistency: Needs Attention
                </h3>
                <p className="text-sm text-neutral-400">
                  88% consistency. Found 3 locations with address format variations. Recommend standardization.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-primary-500/10 border border-primary-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Phone className="w-5 h-5 text-primary-400 mt-1" />
              <div>
                <h3 className="text-primary-400 font-semibold mb-1">
                  Phone Consistency: Good
                </h3>
                <p className="text-sm text-neutral-400">
                  95% consistency. All phone numbers follow standard format with country code.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-neutral-800">
          <Button variant="secondary">
            Run Full NAP Audit
          </Button>
        </div>
      </GlassCard>
    </div>
  );
};

export default StoreManagement;
